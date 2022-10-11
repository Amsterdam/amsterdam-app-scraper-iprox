import requests
from GenericFunctions.Logger import Logger
from GenericFunctions.Hashing import Hashing
from GenericFunctions.TextSanitizers import TextSanitizers


class IproxProjects:
    """ Fetch all projects from IPROX-endpoint and convert the data into a suitable format. The format is described in:
        amsterdam_app_api.models.Projects

        Unique identifiers in Iprox: itmidt
        Get page via unique identifier:

            https://amsterdam.nl/@{itmidt}/page/?new_json=true&pager_rows=1000      (list of pages)
            https://amsterdam.nl/@{itmidt}/page/?AppIdt=app-pagetype&reload=true    (single page)
    """
    def __init__(self, path, project_type):
        self.logger = Logger()
        self.protocol = 'https://'
        self.domain = 'www.amsterdam.nl'
        self.path = path
        self.project_type = project_type
        self.query_params = '?new_json=true&pager_rows=1000'
        self.url = '{protocol}{domain}{path}{query_params}'.format(protocol=self.protocol,
                                                                   domain=self.domain,
                                                                   path=self.path,
                                                                   query_params=self.query_params)
        self.raw_data = list()
        self.parsed_data = list()

    def get_data(self):
        """
        request data from data-end point

        :return: void
        """
        try:
            result = requests.get(self.url)
            self.raw_data = result.json()
        except Exception as error:
            self.logger.error('failed fetching data from {url}: {error}'.format(url=self.url, error=error))

    def parse_data(self):
        """
        Convert data from end-point based on the amsterdam_app_api.models.Projects model

        :return: void
        """
        for i in range(0, len(self.raw_data), 1):
            try:
                # Using md5 will yield the same result for a given string on repeated iterations, hence an identifier
                identifier = self.raw_data[i].get('itmidt', None)
                title = self.raw_data[i].get('title', '').split(':')
                subtitle = None if len(title) == 1 else TextSanitizers.sentence_case("".join([title[i] for i in range(1, len(title))]))
                self.parsed_data.append(
                    {
                        'project_type': self.project_type,
                        'identifier': identifier,
                        'district_id': -1,  # this will be fetched on a successive call...
                        'district_name': '',  # this will be fetched on a successive call...
                        'title': title[0],
                        'subtitle': subtitle,
                        'content_html': TextSanitizers.rewrite_html(self.raw_data[i].get('content', '')),
                        'content_text': TextSanitizers.strip_html(self.raw_data[i].get('content', '')),
                        'images': [],  # these will be fetched on a successive call...
                        'publication_date': self.raw_data[i].get('publication_date', ''),
                        'modification_date': self.raw_data[i].get('modification_date', ''),
                        'source_url': 'https://amsterdam.nl/@{identifier}/page/?AppIdt=app-pagetype&reload=true'.format(identifier=identifier)
                    }
                )
            except Exception as error:
                self.logger.error('failed parsing data from {url}: {error}'.format(url=self.url, error=error))
