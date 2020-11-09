
#@cache_page(60) 整页缓存60s
from django.core.cache import cache

def mycache(expire):
    def _mycache(func):
        def wapper(request,*args,**kwargs):
            ##根据缓存需求设置
            # 1.在这儿先不考虑对某个文章详情的缓存
            if 't_id' in request.GET.keys():
                return func(request, *args, **kwargs)
            # 2. 考虑对文章列表页的缓存
            # 2.1 检查访客身份
            visitor_username = get_user_by_request(request)
            author_username = kwargs['author_id']
            print('visitor is %s,author is %s' % (visitor_username, author_username))
            if visitor_username == author_username:
                cache_key = 'topic_cache_self_%s' % (request.get_full_path())
            else:
                cache_key = 'topic_cache_%s' % (request.get_full_path())
            print('--cache key is %s' % (cache_key))
            # 以下代码体现我们学习过的缓存思想
            res = cache.get(cache_key)
            if res:
                print('--cache in--')
                return res
            # 缓存中无数据，调用视图函数走视图
            res = func(request, *args, **kwargs)
            # 视图结果保存到缓存中
            cache.set(cache_key, res, expire)
            return res
        return wapper
    return _mycache

def get_user_by_request():
    #tool里面有
    pass
#写在视图函数中
def delete_all_cache(request):
    #cache.delete_many()
    #括号内放缓存键名
    #在所有数据更新的时候要删除缓存
    pass