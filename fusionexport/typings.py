typings = {
    "chartConfig": {
        "type": "string",
        "supportedTypes": ["string", "object", "file"],
        "converter": "ChartConfigConverter"
    },
    "inputSVG": {
        "type": "string",
        "supportedTypes": ["file"],
        "converter": "FileConverter"
    },
    "template": {
        "type": "string",
        "supportedTypes": ["string"],
        "converter": "HtmlConverter"
    },
    "templateFilePath": {
        "type": "string",
        "supportedTypes": ["file"],
        "converter": "FileConverter"
    },
    "templateWidth": {
        "type": "integer",
        "supportedTypes": ["string", "integer"],
        "converter": "NumberConverter"
    },
    "templateHeight": {
        "type": "integer",
        "supportedTypes": ["string", "integer"],
        "converter": "NumberConverter"
    },
    "templateFormat": {
        "type": "string",
        "supportedTypes": ["enum"],
        "converter": "EnumConverter",
        "dataset": [
            "Letter",
            "Legal",
            "Tabloid",
            "Ledger",
            "A0",
            "A1",
            "A2",
            "A3",
            "A4",
            "A5"
        ]
    },
    "callbackFilePath": {
        "type": "string",
        "supportedTypes": ["file"],
        "converter": "FileConverter"
    },
    "asyncCapture": {
        "type": "boolean",
        "supportedTypes": ["string", "boolean"],
        "converter": "BooleanConverter"
    },
    "maxWaitForCaptureExit": {
        "type": "integer",
        "supportedTypes": ["string", "integer"],
        "converter": "NumberConverter"
    },
    "dashboardLogo": {
        "type": "string",
        "supportedTypes": ["file"]
    },
    "dashboardHeading": {
        "type": "string",
        "supportedTypes": ["string"]
    },
    "dashboardSubheading": {
        "type": "string",
        "supportedTypes": ["string"]
    },
    "outputFile": {
        "type": "string",
        "supportedTypes": ["string"]
    },
    "type": {
        "type": "string",
        "supportedTypes": ["enum"],
        "converter": "EnumConverter",
        "dataset": [
            "jpeg",
            "jpg",
            "png",
            "pdf",
            "svg",
            "html",
            "csv",
            "xls",
            "xlsx"
        ]
    },
    "quality": {
        "type": "string",
        "supportedTypes": ["enum"],
        "converter": "EnumConverter",
        "dataset": [
            "good",
            "better",
            "best"
        ]
    },
    "headerEnabled": {
        "type": "string",
        "supportedTypes": ["string"]
    },
    "footerEnabled": {
        "type": "string",
        "supportedTypes": ["string"]
    },
    "headerComponents": {
        "type": "string",
        "supportedTypes": ["string", "object"],
        "converter": "ObjectConverter"
    },
    "footerComponents": {
        "type": "string",
        "supportedTypes": ["string", "object"],
        "converter": "ObjectConverter"
    },
    "pageMargin": {
        "type": "string",
        "supportedTypes": ["string", "object"],
        "converter": "ObjectConverter"
    },
    "outputFileDefinition": {
        "type": "string",
        "supportedTypes": ["file"],
        "converter": "FileConverter"
    },
    "resourceFilePath": {
        "type": "string",
        "supportedTypes": ["file"],
        "converter": "FileConverter"
    }
}
