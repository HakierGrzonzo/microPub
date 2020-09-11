import zipfile
from bs4 import BeautifulSoup as Soup
from bs4 import Tag
import re

class Epub():
    def __init__(self, filename):
        try:
            self.file = zipfile.ZipFile(filename, "r")
            mimetype = self.file.read("mimetype").decode("UTF-8")
            if mimetype != "application/epub+zip":
                print("This file is not a valid epub file!")
                raise Exception("File not valid!")
        except Exception as e:
            print(e)
            raise Exception("File not valid!")

        # get content.opf and try to get toc.ncx
        self.prefix =  str()
        tocFile = False # if toc does not exist
        contentFile = None
        for filename in self.file.namelist():
            if filename.endswith("content.opf"):
                contentFile = self.file.read(filename).decode("UTF-8")
                if filename != "content.opf":
                    self.prefix = filename[:-len("content.opf")]
            elif filename.endswith("volume.opf"):
                contentFile = self.file.read(filename).decode("UTF-8")
                if filename != "volume.opf":
                    self.prefix = filename[:-len("volume.opf")]
            elif filename.endswith("toc.ncx"):
                tocFile = self.file.read(filename).decode("UTF-8")
        if not contentFile:
            raise Exception("File not valid, no content.opf found!")
        contentSoup = Soup(contentFile, features="lxml")

        # get title from ebook
        try:
            self.title = contentSoup.find("dc:title").text
        except:
            # if ebook has no title?
            self.title = "An intresting ebook without a title"

        # parse <manifest> in content.opf
        self.id_to_file = dict()
        for itemref in contentSoup.find("manifest").children:
            if isinstance(itemref, Tag):
                self.id_to_file[itemref["id"]] = itemref["href"]

        self.files = dict()
        # parse <spine>
        self.spine = list()
        for itemref in contentSoup.find("spine").children:
            if isinstance(itemref, Tag):
                href = self.id_to_file[itemref["idref"]]
                content = self.file.read(self.prefix + href).decode("UTF-8")
                item = EpubItem(href, content)
                self.spine.append(item)
                self.files[href] = item

        # parse toc.ncx
        if tocFile:
            tocFile = False # TODO: parse toc

    def get(self, href, relative_to = None):
        if relative_to and "/" in relative_to:
            relPath = relative_to.split("/")[:-1]
            path = href
            href = ""
            for x in relPath:
                href += x + "/"
            href += path
        
        href = re.sub(r"[^\/]+\/\.\.\/", "", href)
        print(href)

        try:
            return self.files[href].content
        except KeyError:
            try:
                content = self.file.read(self.prefix + href).decode("UTF-8")
                self.files[href] = EpubItem(href, content)
                return content
            except:
                raise FileNotFoundError("{} does not exist in this epub".format(self.prefix + href))
            

class EpubItem:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content


        