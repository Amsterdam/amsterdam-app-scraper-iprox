""" Mock data file """
# pylint: disable=line-too-long


class TestData:
    """ Mock data class """
    def __init__(self):
        self.image_download_jobs = [
            {
                'url': 'valid_url',
                'image_id': '0',
                'filename': 'mock0.jpg',
                'description': '',
                'size': 'orig'
            },
            {
                'url': 'invalid_url',
                'image_id': '1',
                'filename': 'mock1.jpg',
                'description': '',
                'size': 'orig'
            },
            {
                'url': 'valid_url',
                'image_id': '1',
                'filename': 'fail_saving.jpg',
                'description': '',
                'size': 'orig'
            }
        ]

        self.iprox_recursion = {
            "Nam": "Target",
            "cluster": [
                {"Nam": "Target", "cluster": [{"Nam": "Target", "veld": []}]},
                {"Nam": "Target", "cluster": {"Nam": "Target", "veld": {}}},
                {"Nam": "Invalid Target", "cluster": {}}
            ]
        }

        self.iprox_stadsloketten = {
            "item": {
                "page": {
                    "pagetype": "subhome",
                    "cluster": [
                        {
                            "Nam": "Blok",
                            "cluster": [
                                {
                                    "Nam": "Superlink",
                                    "cluster": [
                                        {
                                            "Nam": "Verwijzing",
                                            "cluster": {
                                                "Nam": "Intern",
                                                "veld": [
                                                    {
                                                        "Nam": "Link",
                                                        "Wrd": "loketten",
                                                        "link": {
                                                            "Url": "https://sub-page/"
                                                        },
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Titel",
                                                    "Wrd": "contact",
                                                },
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }

        self.iprox_stadsloketten_ingest_fail = {
            "item": {
                "page": {
                    "pagetype": "subhome",
                    "cluster": [
                        {
                            "Nam": "Blok",
                            "cluster": [
                                {
                                    "Nam": "Superlink",
                                    "cluster": [
                                        {
                                            "Nam": "Verwijzing",
                                            "cluster": {
                                                "Nam": "Intern",
                                                "veld": [
                                                    {
                                                        "Nam": "Link",
                                                        "Wrd": "FAIL INGEST",
                                                        "link": {
                                                            "Url": "https://sub-page/"
                                                        },
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Titel",
                                                    "Wrd": "FAIL INGEST",
                                                },
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }

        self.iprox_stadsloket = {
            "item": {
                "page": {
                    "pagetype": "subhome",
                    "cluster": [
                        {
                            "Nam": "Meta",
                            "cluster": {
                                "Nam": "Meta",
                                "cluster": [
                                    {
                                        "Nam": "Gegevens",
                                        "veld": [
                                            {
                                                "Nam": "Samenvatting",
                                                "Txt": "text"
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "Nam": "Blok",
                            "cluster": [
                                {
                                    "Nam": "Afbeelding",
                                    "cluster": [
                                        {
                                            "Nam": "Afbeelding",
                                            "veld": [
                                                {
                                                    "Nam": "Afbeelding",
                                                    "FilNam": "test_orig.jpg",
                                                    "Src": {
                                                        "_": "/1/2/3/test_orig.jpg"
                                                    },
                                                    "asset": [
                                                        {
                                                            "FilNam": "test.jpg",
                                                            "Src": {
                                                                "_": "/1/2/3/1px/text.jpg"
                                                            }
                                                        },
                                                        {
                                                            "FilNam": None,
                                                            "Src": {
                                                                "_": None
                                                            }
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Leestekst",
                                    "veld": [
                                        {
                                            "Nam": "Titel",
                                            "Wrd": "Stadsloket Centrum",
                                        },
                                        {
                                            "Nam": "Tekst",
                                            "Txt": "text",
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Titel",
                                                    "Wrd": "Openingstijden",
                                                },
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text",
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text",
                                                },
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Lijst",
                                    "cluster": [
                                        {
                                            "Nam": "Omschrijving",
                                            "veld": [
                                                {
                                                    "Nam": "Titel",
                                                    "Wrd": "Mailen",
                                                },
                                                {
                                                    "Nam": "Tekst",
                                                    "Txt": "text",
                                                },
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }

        self.iprox_project_detail = [
            {'Gegevens': [{'Nam': 'Auteur', 'Wrd': 'Mischa Tiebie'}, {'Nam': 'Basis afbeelding', 'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/mock.jpg'}, 'Txt': '<div>mock</div>', 'asset': [{'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/220px/mock.jpg'}}, {'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/80px/mock.jpg'}}, {'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/orig/mock.jpg'}}]}]},
            {'Kenmerken': {'Nam': 'Kenmerk', 'Wrd': 'Centrum', 'Src': 'Stadsdeel', 'SelWrd': 'Centrum', 'item': {'SelItmIdt': '5398', 'Wrd': 'Centrum'}}},
            {'Afbeelding': [{'Nam': 'Afbeelding', 'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/mock.jpg'},'Txt': '<div>mock</div>', 'asset': [{'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/220px/mock.jpg'}}, {'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/700px/mock.jpg'}}, {'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/460px/mock.jpg'}}, {'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/80px/mock.jpg'}}]}]},
            {'Afbeelding': {'Nam': 'Afbeelding', 'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/mock.jpg'}, 'Txt': '<div>mock</div>', 'asset': [{'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/220px/mock.jpg'}}]}},
            {'Omschrijving': [{'Nam': 'Titel', 'Wrd': 'Wat gaan we doen'}, {'Nam': 'Tekst', 'Txt': '<div>mock</div>'}, {'Nam': 'App categorie', 'SelWrd': 'Wat', 'SelAka': 'what', 'item': {'SelItmIdt': '7055', 'Wrd': 'Wat', 'Aka': 'what'}}]},
            {'Omschrijving': [{'Nam': 'Titel', 'Wrd': 'Meer informatie'}, {'Nam': 'Tekst', 'Txt': '<div>mock</div>'}, {'Nam': 'App categorie', 'SelWrd': 'Meer info', 'SelAka': 'more-info', 'item': {'SelItmIdt': '7059', 'Wrd': 'Meer info', 'Aka': 'more-info'}}]},
            {'Omschrijving': [{'Nam': 'Titel', 'Wrd': 'Contact'}, {'Nam': 'Tekst', 'Txt': '<div>mock</div'}, {'Nam': 'App categorie', 'SelWrd': 'Contact', 'SelAka': 'contact', 'item': {'SelItmIdt': '7057', 'Wrd': 'Contact', 'Aka': 'contact'}}]},
            {'Gegevens': [{'Nam': 'Auteur', 'Wrd': 'mock'},{'Nam': 'Basis afbeelding', 'FilNam': 'mock.jpg', 'Src': {'resolved': 'true', '_': '/publish/pages/000000/mock.jpg'}, 'Txt': '<div>mock</div>', 'asset': [{'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/220px/mock.jpg'}},{'FilNam': 'mock.jpg', 'Src': {'_': '/publish/pages/000000/80px/mock.jpg'}}]},{'Nam': 'Samenvatting', 'Txt': '<div>mock</div>'}]},
            {'Omschrijving': [{'Nam': 'Titel', 'Wrd': 'Wat gaat er gebeuren'}, {'Nam': 'Tekst', 'Txt': '<div>mock</div>'}, {'Nam': 'App categorie', 'SelWrd': 'Wat', 'SelAka': 'what', 'item': {'SelItmIdt': '7055', 'Wrd': 'Wat', 'Aka': 'what'}}]},
            {'Omschrijving':[{'Nam': 'Titel', 'Wrd': 'Maatregelen en gevolgen'}, {'Nam': 'Tekst', 'Txt': '<div>mock</div>'}, {'Nam': 'App categorie', 'SelWrd': 'Werkzaamheden / Maatregelen', 'SelAka': 'work', 'item': {'SelItmIdt': '7062', 'Wrd': 'Werkzaamheden / Maatregelen', 'Aka': 'work'}}]},
            {'Omschrijving': [{'Nam': 'Titel', 'Wrd': 'Renoveren brug'}, {'Nam': 'Tekst', 'Txt': '<div>mock</div>'},{'Nam': 'App categorie', 'SelWrd': 'Werkzaamheden / Maatregelen', 'SelAka': 'work', 'item': {'SelItmIdt': '7062', 'Wrd': 'Werkzaamheden / Maatregelen', 'Aka': 'work'}}]},
            {'Omschrijving': [{'Nam': 'Titel', 'Wrd': 'Wanneer', 'script': {'type': 'text/javascript'}, 'style': {'resolved': 'true'}}, {'Nam': 'Kleine kop', 'Wrd': '0', 'script': {'type': 'text/javascript'}, 'style': {'resolved': 'true'}}, {'Nam': 'Tekst', 'Txt': '<div>mock</div>'}, {'Nam': 'App categorie', 'SelWrd': 'Wanneer/ Planning', 'SelAka': 'when', 'item': {'SelItmIdt': '7063', 'Wrd': 'Wanneer/ Planning', 'Aka': 'when'}}]},
            {'Coordinaten': {'Nam': 'Coordinaten', 'Txt': {'geo': {'json': [{'type': 'EPSG:4326', '_': '{"type":"FeatureCollection","features":[{"geometry":{"coordinates":[4.918909612586674,52.367703897750914]}}]}'}]}}}},
            {'Koppeling': [{'Nam': 'Titel', 'Wrd': 'Nieuws'},{'Nam': 'Link', 'Wrd': 'Meer nieuws', 'link': {'pagetype': 'index', 'Url': 'https://mock_nieuws/'}},{'Nam': 'App categorie', 'SelWrd': 'Nieuws', 'SelAka': 'news','item': {'SelItmIdt': '7058', 'Wrd': 'Nieuws', 'Aka': 'news'}}]}
        ]

        self.iprox_project_details = {
            'identifier': 'identifier',
            'body': {'contact': [{'title': 'Contact', 'html': '<div>mock</div', 'text': 'mock</div'}],
                     'what': [{'title': 'Wat gaan we doen', 'html': '<div>mock</div>', 'text': 'mock'},
                              {'title': 'Wat gaat er gebeuren', 'html': '<div>mock</div>', 'text': 'mock'}],
                     'when': [{'title': 'Wanneer', 'html': '<div>mock</div>', 'text': 'mock'}],
                     'where': [],
                     'work': [{'title': 'Maatregelen en gevolgen', 'html': '<div>mock</div>', 'text': 'mock'},
                              {'title': 'Renoveren brug', 'html': '<div>mock</div>', 'text': 'mock'}],
                     'more-info': [{'title': 'Meer informatie', 'html': '<div>mock</div>', 'text': 'mock'}],
                     'timeline': {}},
            'coordinates': {'lon': 4.918909612586674, 'lat': 52.367703897750914},
            'contacts': [],
            'district_id': 5398, 'district_name': 'Centrum',
            'images': [{'type': '',
                        'sources': {
                            '220px': {'url': 'https://www.amsterdam.nl/publish/pages/000000/220px/mock.jpg', 'image_id': '3f4a4ec3bc10f60d3aa2eac9b742c8ec', 'filename': 'mock.jpg', 'description': ''},
                            '700px': {'url': 'https://www.amsterdam.nl/publish/pages/000000/700px/mock.jpg', 'image_id': 'a8c4ef5dce6fea7132ebcbb52e1124c9', 'filename': 'mock.jpg', 'description': ''},
                            '460px': {'url': 'https://www.amsterdam.nl/publish/pages/000000/460px/mock.jpg', 'image_id': '479b05b93eaef5fd57aa2a202bf103b9', 'filename': 'mock.jpg', 'description': ''},
                            '80px': {'url': 'https://www.amsterdam.nl/publish/pages/000000/80px/mock.jpg', 'image_id': 'aa70389feb4f9b7c2184334a2daa8e86', 'filename': 'mock.jpg', 'description': ''},
                            'orig': {'url': 'https://www.amsterdam.nl/publish/pages/000000/mock.jpg', 'image_id': 'e51353040e4c049559c975ce6a650947', 'filename': 'mock.jpg', 'description': ''}}},
                       {'type': '',
                        'sources': {
                            '220px': {'url': 'https://www.amsterdam.nl/publish/pages/000000/220px/mock.jpg', 'image_id': '3f4a4ec3bc10f60d3aa2eac9b742c8ec', 'filename': 'mock.jpg', 'description': ''},
                            'orig': {'url': 'https://www.amsterdam.nl/publish/pages/000000/mock.jpg', 'image_id': 'e51353040e4c049559c975ce6a650947', 'filename': 'mock.jpg', 'description': ''}}}],
            'news': [{'identifier': '000000-news', 'project_identifier': 'identifier', 'url': 'https://amsterdam.nl/@000000-news/page/?AppIdt=app-pagetype&reload=true'}],
            'page_id': -1,
            'title': '', 'subtitle': None,
            'rel_url': 'mock/mock', 'url': 'https://mock/mock/mock/'
        }

        self.iprox_projects = [{
            "category": "Mock",
            "itmidt": '000000-projects',
            "feedid": "https://mock/",
            "publication_date": "1970-01-01",
            "modification_date": "1970-01-01",
            "image_url": "https://mock",
            "title": "mock: data",
            "content": "<div><p>mock</p></div>",
            "source_url": "https://mock",
            "related_articles": "",
            "author": "",
            "photo_author": "",
            "images": []
        }]

        self.news_data = [{
            'category': 'Algemeen',
            'feedid': 'https://www.amsterdam.nl/nieuws/mock/',
            'itmidt': '000000-news',
            'publication_date': '1970-01-01',
            'modification_date': '1970-01-01',
            'image_url': 'https://www.amsterdam.nl/publish/pages/000000/mock.jpg',
            'title': 'mock',
            'content': 'mock',
            'source_url': 'https://mock/',
            'related_articles': '',
            'author': '',
            'photo_author': '',
            'images': ['https://mock.jpg']}]

        self.timeline_raw = {
            "item": {
                "Url": "https://mock/mock/mock/",
                "relUrl": "mock/mock",
                "page": {
                    "pagetype": "tijdlijn",
                    "title": "Tijdlijn",
                    "cluster": [
                        {
                            "Nam": "Meta",
                            "cluster": [
                                {
                                    "Nam": "Hoofditem",
                                    "cluster": [
                                        {
                                            "Nam": "Inhoud",
                                            "veld": {
                                                "Nam": "Inleiding",
                                                "Txt": "<div>mock</div>",
                                            }
                                        },
                                        {
                                            "Nam": "Gegevens",
                                            "veld": {
                                                "Nam": "Inleiding",
                                                "Txt": "<div>mock</div>",
                                            }
                                        }
                                    ]
                                },
                                {
                                    "Nam": "Hoofditem",
                                    "cluster": [
                                        {
                                            "Nam": "Eigenschappen",
                                            "veld": {
                                                "Nam": "Titel",
                                                "Wrd": "mock",
                                            }
                                        },
                                        {
                                            "Nam": "Instellingen",
                                            "SelWrd": "mock",
                                            "veld": {
                                                "Nam": "Subitems initieel ingeklapt",
                                                "Wrd": "1",
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
