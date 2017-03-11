function get_list_sql()
	local sql = 'select a.id,a.title,a.summary,a.create_time,a.category_id,a.publish_year,a.publish_month,publish_date,a.comment_count,a.path,b.name from blog_article a,blog_category b where a.category_id = b.id'
	if ngx.var.category ~= '' then
		sql = sql .. " and b.name = " .. ngx.quote_sql_str(ngx.var.category)
	end
	if ngx.var.year ~= '' then
		sql = sql .. " and a.publish_year = " .. ngx.quote_sql_str(ngx.var.year)
	end
	if ngx.var.month ~= '' then
		sql = sql .. " and a.publish_month = " .. ngx.quote_sql_str(ngx.var.month)
	end
	sql = sql .. ' order by a.create_time desc'
	return sql
end

function get_count_sql(sql)
	s,_ = string.find(sql,'from')
	e,_ = string.find(sql,'order')
	return 'select count(*) as count ' .. string.sub(sql,s,e-2)
end

function pagination(cur_page,page_count)
    if page_count <= 1 then return '' end
    local res = {}
    table.insert(res,'<nav style="text-align:right;">')
    table.insert(res,'<ul class="pagination">')
    if cur_page == 1 then
        table.insert(res,'<li class="disabled"><span>&laquo;</span></li>')
    else
        table.insert(res,'<li><a href="'.. ngx.var.url .. 'page/1">&laquo;</a></li>')
    end
    local page_start,page_end = 1,page_count
    if page_count > 5 then
        page_start = math.max(cur_page-2,1)
        page_end = page_start + 4
        if page_end > page_count then
            page_start = page_start - (page_end - page_count)
            page_end = page_start + 4
        end
    end
    for i = page_start,page_end do
        if i == cur_page then
            table.insert(res,string.format('<li class="active"><span>%d</span></li>',i))
        else
            table.insert(res,string.format('<li><a href="'.. ngx.var.url .. 'page/%d">%d</a></li>',i,i))
        end
    end
    if cur_page == page_count then
        table.insert(res,'<li class="disabled"><span>&raquo;</span></li>')
    else
        table.insert(res,string.format('<li><a href="'.. ngx.var.url .. 'page/%d">&raquo;</a></li>',page_count))
    end
    table.insert(res,'</ul>')
    table.insert(res,'</nav>')
    return table.concat(res)
end

local mysql = require("resty.mysql_pool")
local list_sql = get_list_sql()
local count_sql = get_count_sql(list_sql)
local flag,res = mysql:query(count_sql)
if not flag then
   	return
end
local cur_page,page_size,start_row_index,end_row_index = 1,10,0,10
local page_count = math.ceil(res[1].count / page_size)
if ngx.var.page ~= '' then
	cur_page = tonumber(ngx.var.page)
	cur_page = math.min(page_count,math.max(cur_page,1))
	start_row_index,end_row_index = (cur_page - 1) * page_size,cur_page * page_size
end
local pagination = pagination(cur_page,page_count)
list_sql = string.format('%s limit %d,%d',list_sql,start_row_index,end_row_index)
local flag,article_list = mysql:query(list_sql)
if not flag then
   	return
end
--recent_post_article
flag,recent_list = mysql:query('select id,title,path from blog_article order by create_time desc limit 5')
if not flag then
   	return
end
--archives
flag,archives_list = mysql:query('select publish_year,publish_month,count(*) as total from blog_article group by publish_year,publish_month order by create_time desc')
if not flag then
   	return
end
--category
flag,category_list = mysql:query('select * from blog_category a,(SELECT category_id, count(*) total FROM blog_article GROUP BY category_id) b where a.id = b.category_id order by total desc')
if not flag then
   	return
end
mysql:close()
local template = require("resty.template")
local context = {title = 'Fred Zhang的个人博客',article_list = article_list,recent_list = recent_list,archives_list = archives_list,category_list = category_list,pagination = pagination}
template.render("template/index.html",context)