#!/usr/bin/env python3

from typing import Optional

from praw.models import Submission

from bulkredditdownloader.site_authenticator import SiteAuthenticator
from bulkredditdownloader.resource import Resource
from bulkredditdownloader.site_downloaders.base_downloader import BaseDownloader


class Direct(BaseDownloader):
    def __init__(self, post: Submission):
        super().__init__(post)

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        return [Resource(self.post, self.post.url)]
