import re
from datetime import datetime
from typing import List, Optional

from lxml.cssselect import CSSSelector

from src.parser.html_parser import ArticleBody, BaseParser, attribute
from src.parser.html_parser.utility import (
    extract_article_body_with_selector,
    generic_author_parsing,
    generic_date_parsing,
    generic_topic_parsing,
)


class FreeBeaconParser(BaseParser):
    _paragraph_selector = CSSSelector(".article-content > p")

    @attribute
    def body(self) -> ArticleBody:
        return extract_article_body_with_selector(
            self.precomputed.doc,
            paragraph_selector=self._paragraph_selector,
        )

    @attribute
    def authors(self) -> List[str]:
        return generic_author_parsing(self.precomputed.meta.get("author"))

    @attribute
    def publishing_date(self) -> Optional[datetime]:
        return generic_date_parsing(self.precomputed.ld.bf_search("datePublished"))

    @attribute
    def title(self) -> Optional[str]:
        return self.precomputed.ld.bf_search("headline")

    @attribute
    def topics(self) -> List[str]:
        topics: Optional[List[str]] = self.precomputed.ld.bf_search("keywords")
        return topics if topics else []