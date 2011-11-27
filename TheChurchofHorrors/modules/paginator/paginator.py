# coding=utf-8

class Paginator:

    def __init__(self,query,page_length,page):
        self.query = query
        self.page_length = page_length
        try:
            self.page = int(page)
            if self.page <=0: self.page = 0
        except ValueError,TypeError:
            self.page = 0
    
    def current(self):
        if not self.page:
            return ()
        
        idx1 = (self.page-1)*self.page_length
        idx2 = self.page*self.page_length
        
        if not self.query[idx1:idx2].count():
            return ()
        
        return self.query[idx1:idx2]
        
    
    def next(self):
        if not self.page:
            return None
        
        idx1 = self.page*self.page_length
        idx2 = (self.page+1)*self.page_length
        
        if not self.query[idx1:idx2].count():
            return None
        
        
        return "?p=%d" % (self.page+1)
    
    def prev(self):
        if self.page <=1:
            return None
        
        idx1 = (self.page-2)*self.page_length
        idx2 = (self.page-1)*self.page_length
        
        if not self.query[idx1:idx2].count():
            return None
        
        return "?p=%d" % (self.page-1) if (self.page-1) > 1 else ""
        
    def hasprev(self):
        if self.page <=1:
            return False
        
        idx1 = (self.page-2)*self.page_length
        idx2 = (self.page-1)*self.page_length
        
        if self.query[idx1:idx2].count():
            return True
