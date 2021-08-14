class Production:
    def __init__(self, title, slug, developer, platform, typetag, screenshots, files,
    lic, assetLicense="", description="", video="", date="", tags=[], alias="", repository="", gameWebsite="", devWebsite="", onlineplay="",
    wip="", url = ""):
        # mandatory fields
        self.title = title
        self.slug = slug
        self.developer = developer
        self.platform = platform
        self.typetag = typetag
        self.screenshots = screenshots
        self.files = files

        # optional fields
        self.lic = lic if lic else ""
        self.assetLicense = assetLicense if assetLicense else ""
        self.description = description if description else ""
        self.video = video if video else ""
        self.date = date if date else ""
        self.tags = tags if tags is not None else []
        self.alias = alias if alias is not None else []
        self.repository = repository if repository else ""
        self.gameWebsite = gameWebsite if gameWebsite else ""
        self.devWebsite = devWebsite if devWebsite else ""
        self.onlineplay = onlineplay if onlineplay else ""
        self.wip = wip if wip else ""

        self.url = url