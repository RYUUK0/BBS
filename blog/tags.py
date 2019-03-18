import copy


#制定一个自定义分页类
class MyPage(object):
    def __init__(self, page_num, page_count, data_list, data_length, get_dict = None ):
        """
        :param page_num: 输入的页码
        :param page_count: 每页的数据条数
        :param all_count: 总行数
        :param data_list: 数据列表
        :param get_dict: 传入的页面筛选条件
        """
        try:
            self.page_num = int(page_num)
        except Exception as e:
            self.page_num = 1
        self.page_count = page_count
        self.all_count = data_length
        self.data_list = data_list

        #求出页码最大边界max_page
        max_page, b = divmod(self.all_count, page_count)
        self.max_page = max_page
        if b:
            self.max_page = max_page + 1


        #给出页码为+-2， 共5个,筛选出在页码范围之内的数字
        page_range = []
        for i in range(5):
            c = self.page_num + i - 2
            if c > 0 and c <= self.max_page:
                page_range.append(c)
        self.page_row = page_range

        #上一页的页码和下一页的页码:
        self.prev = self.page_num - 1
        self.next = self.page_num + 1

        self.get_dict = copy.deepcopy(get_dict) or {}

    #得到页面的筛选条件,并添加到URL中
    def get_url(self):
        res_url = ""
        for key, value in self.get_dict.items():
            if key != 'page':
                res_url += "&%s=%s"%(key, value)
        return res_url
    #判断是否有上一页
    def prev_page(self):
        if self.page_num - 1:
            return True
        else:
            return False
    def next_page(self):
        if self.next <= self.max_page:
            return True
        else:
            return False

    #得出开始和结束的数据条数
    @property
    def start(self):
        return (self.page_num - 1) * self.page_count

    @property
    def end(self):
        return (self.page_num) * self.page_count

    #获取页面内容
    @property
    def content(self):
        return self.data_list[self.start: self.end]