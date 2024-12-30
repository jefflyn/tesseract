

def generate_member_model_insert(start_id=1, days=[], hours=[]):
    model_id = start_id
    right_config = []
    for role in ["老板", "员工"]:
        expiry_time = 0 if role == '老板' else 180
        role_id = 1 if role == '老板' else 3
        for times in days:
            for hour in hours:
                right_name = "每日免费" + str(times) + "单" + str(hour) + "小时"
                model_name = role + "-" + right_name
                right_value = 60*hour
                model_sql = ("INSERT INTO lhc_member_model (id, model_name, model_type, model_icon, model_priority, expiry_time, create_time, deleted, update_time, origin_price, price, renewal_price, remark, first_discount, buy_img, bg_img) "
                             "VALUES (" + str(model_id) + ", '" + model_name +"', 1, 'https://img3.dian.so/lhc/2020/11/26/154w_51h_6BBE51606372504.gif', 0, " + str(expiry_time) + ", now(), 1, now(), null, null, null, null, null, null, 'https://img3.dian.so/lhc/2021/04/16/1038w_660h_FA0B81618565445.png');")
                right_sql = ("INSERT INTO member_rights (rights, rights_name, rights_value, model_id, create_time, update_time, deleted, ext_param) "
                             "VALUES ('3', '"+right_name+"', '"+str(right_value)+"', "+ str(model_id) +", now(), now(), 0, '{\"free_count\":\"" + str(times) +"\",\"icon_select\":\"https://img3.dian.so/lhc/2021/04/29/126w_126h_71D861619691858.png\",\"remark\":\"充电宝特权\"}');")
                # print(model_id, times, hour)
                print(model_sql, right_sql)
                print(right_sql)
                config_sql = ("INSERT INTO member_model_rights_map (role_id, rights_key, model_id, deleted, gmt_create, gmt_update) VALUES ("
                              + str(role_id) + ", '" + str(times) + "_" + str(hour) + "', " + str(model_id) + ", 0, now(), now());")
                right_config.append(config_sql)
                model_id += 1
    for sql in right_config:
        print(sql)


if __name__ == '__main__':
    generate_member_model_insert(200, days=[1,2,3,4,5], hours=list(range(1,11)))
