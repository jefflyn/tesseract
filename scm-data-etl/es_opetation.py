from elasticsearch import Elasticsearch

# elasticsearch集群服务器的地址
# 创建elasticsearch客户端
es = Elasticsearch(
    "http://elasticsearch762.dian-dev.com:9200",
    # # 启动前嗅探es集群服务器
    # sniff_on_start=True,
    # # es集群服务器结点连接异常时是否刷新es节点信息
    # sniff_on_connection_fail=True,
    # # 每60秒刷新节点信息
    # sniffer_timeout=60
)


def add_field(index, body):
    """将现有 index 增加一个字段

    Args:
        index (str): 索引名称
        body (dict): 查询体同上 PUT /zq_test/_mapping
    """
    return es.indices.put_mapping(index=index, body=body)


if __name__ == '__main__':
    resp = es.info()
    print(resp)
    # dict_field = {}
    add_field('dispatch_shop_flink', {"properties": {"pb_dispatch_disable": {"type": "integer"}}})
