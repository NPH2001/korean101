from typing import Any, List, Union
from scrapy.http import Request, Response
from scrapy.pipelines.files import FilesPipeline
import scrapy
from itemloaders import ItemAdapter
from scrapy.pipelines.media import MediaPipeline
from spiders.util import cookie_util
from itemloaders import ItemAdapter
import os


class CustomFilePipelines(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None) -> str:
        file_path = item.get('file_path')
        file_name = item.get('file_name')
        return os.path.join(file_path, file_name)

    def get_media_requests(self, item, info):
        if 'file_urls' not in item:
            return
        adapter = ItemAdapter(item)

        cookies = cookie_util.get_cookies()

        for file_url in adapter.get('file_urls', []):
            yield Request(file_url,
                          cookies=cookies,)
