import scrapy


class test:
    pass

if __name__ == "__main__":
    for item in dir(scrapy.Item):
        if item not in dir(scrapy.item.DictItem):
            print(item)
            print(type(item))
    #print(dir(test))

