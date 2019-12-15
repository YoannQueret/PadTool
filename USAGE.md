Usage
=====

Introduction
------------

Before executing PadTool, you will need two files :
    - A config file : it defines all the configuration of the radio station and what output to generate
    - A template file : used to compare the json/xml/txt file given in [source]->url, with the tags defined in it. It is used to locate the different info to retrieve. More info below regarding this file 

Config file
-----------

A PadTool config file is divided in 5 sections :
    - General : mandatory, info regarding the radio station

    example:
        [general]
        mode = standalone
        timer = 10
        radioName = GRRIF
        slogan = déchiRRe ta RRoutine
        logoUrl = https://www.20ans100francs.ch/uploads/partner/logo/4/GRRIFnoir_web.png
        backurl = https://www.grrif.ch/wp-content/themes/grrif/img/home/default.jpg
        theme = template
        colorl = white
        color1 = lightgrey
        color2 = white
        outFolder = ./out/

    The first parameter to define is the mode. PadTool has two modes, `standalone` or `server` (not implemented yet.)
    The attribute timer is mandatory with the standalone mode. This attribute defines the time between two parsing of the file 
    Here the name, the slogan, the URL of the logo are defined. The name and the slogan are displayed in the DLS text when file parsing does not found tags.
    The background URL (backurl) is optional. In several themes, the background image can be defined.
    Theme attribute defines the theme to use for the ATC (Artist, Title & Cover slide). Themes can be found in the `themes` folder
    colorl corresponds to the background color of the logo slide (if generated)
    color1 and color2 corresponds to colors used in the theme (see each theme for more details)
    outFolder defines the output folder for DLS and Slides files.

    - Source : mandatory, defines where to locate the radio info file and the template to use

    example:
        [source]
        url = http://grrif.ch/live/covers.json
        template = examples-template/template-grrif.json
        format = json
        defaultCover = https://www.grrif.ch/Medias/Covers/m/default.jpg
    
    The url parameter defines the file info to parse
    The template is the location of your template file
    The format parameter defines the type of the file (json, xml or txt)
    The default cover is displayed where there is no cover found

    - Proxy (optional)

    example:
        [proxy]
        enabled = 1
        http = http://user:pass@my-super-proxy.fr:8080
        https = https://user:pass@my-super-proxy.fr:8080

    Defines whether the internet traffic must go through a proxy or not.
    The enabled parameter must be defined to 0 (disable) or 1 (enabled)
    http and https parameters are the url of your proxies

    - Slides : mandatory

    example:
        [slides]
        logo = 1
        music = 1

    Defines which slides to generate. 
    Logo corresponds to a slide with a logo of the radio station
    Music corresponds to a slide wit hthe Artist, Title and Cover actually broadcasted.

    - DLS : mandatory, defined DLS generation options

    example:
        [dls]
        enabled = 1
        text = $radioName $slogan avec : $title par $artist

    Enabled attribute defines if PadTool must generate a DLS+ text (0 = disabled; 1 = enabled)
    The text attribute allows to personnalize the DLS with tags:
        $radioName is replaced by the defined name of the radio station
        $slogan is replaced by the defined slogan of the radio station
        $artist is replaced by the artist of the song broadcasted
        $title is replaced by the title of the song broadcasted

    - Filters (optional)

    example:
        [filter]
        title = ["11", "12"]
        artist = ["11", "12"]

    Permits to filter and to not process the string which explicitly contains the text given. 
    It could be given in an array of string.

    Template file
    -------------

    The template file is useful for the software in order to replace the tags $artist, $title and $cover by the values in the file provided in the config file ([source]->url)

    Example, json file provided by a local station from Ardennes, France : RVM
        {"title_str":"","artist":"M.POKORA","title":"SI T ES PAS LA","image":"https:\/\/ftp.rvm.fr\/00009421.jpg","url":"https:\/\/itunes.apple.com\/fr\/album\/default\/id11111app=music&ign-mpt=uo%3D4","time":1576441780}
    The template associated should be then :
        {"title_str":"","artist":"$artist","title":"$title","image":"https:\/\/ftp.rvm.fr\/00009421.jpg","url":"$cover","time":1576441780}

Best Practices
==============
To be completed