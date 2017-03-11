local request_method = ngx.var.request_method
if "GET" == request_method then
    local template = require("resty.template")
    template.render("template/contact.html",{title='联系我'})
elseif "POST" == request_method then
    ngx.req.read_body()
    local args = ngx.req.get_post_args()
    local mysql = require("resty.mysql_pool")
	local sql = string.format("insert into blog_message(name,email,subject,message,create_time) values('%s','%s','%s','%s','%s')",args["name"],args["email"],args["subject"],args["message"],os.date("%Y-%m-%d %H:%M:%S", os.time()))
	local flag = mysql:query(sql)
	if not flag then
   		return
	end
	mysql:close()
	ngx.redirect("/")
end
