import zipfile
from bs4 import BeautifulSoup as Soup
from bs4 import Tag

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

        self.file_to_content = dict()
        # parse <spine>
        self.spine = list()
        for itemref in contentSoup.find("spine").children:
            if isinstance(itemref, Tag):
                href = self.id_to_file[itemref["idref"]]
                content = self.file.read(self.prefix + href).decode("UTF-8")
                self.spine.append(content)
                self.file_to_content[href] = content
                

        # parse toc.ncx
        if tocFile:
            tocFile = False # TODO: parse toc

    def get(self, href):
        try:
            return self.file_to_content[href]
        except KeyError:
            if href in [x[1] for x in self.id_to_file.items()]:
                content = self.file.read(self.prefix + href).decode("UTF-8")
                self.file_to_content[href] = content
            else:
                raise FileNotFoundError("{} does not exist in this epub".format(self.prefix + href))
            

                



        