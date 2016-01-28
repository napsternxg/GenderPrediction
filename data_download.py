# [START all]
import argparse

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials


def main(project_id):
    # [START build_service]
    # Grab the application's default credentials from the environment.
    credentials = GoogleCredentials.get_application_default()
    # Construct the service object for interacting with the BigQuery API.
    bigquery_service = build('bigquery', 'v2', credentials=credentials)
    # [END build_service]

    try:
        # [START run_query]
        query_request = bigquery_service.jobs()
        query_data = {
            'query': 
            """
SELECT a.name, a.Total, a.Female, a.Male, 
GREATEST(a.Male, a.Female) as confidence
FROM
(SELECT name, SUM(number) as Total,
SUM(CASE
  WHEN gender = "F"
  THEN number
  ELSE 0
  END)/Total as Female,
SUM(CASE
  WHEN gender = "M"
  THEN number
  ELSE 0
  END)/Total as Male,
FROM [fh-bigquery:popular_names.usa_1910_2013]  GROUP BY name) as a ORDER BY confidence DESC;
            """
            }

        query_response = query_request.query(
            projectId=project_id,
            body=query_data).execute()
        # [END run_query]

        # [START print_results]
        file_name="data/name_gender.tsv"
        print('Query Results stored in: %s' % file_name)
        with open(file_name, "wb+") as fp:
            for row in query_response['rows']:
                print >> fp, '\t'.join(field['v'] for field in row['f'])
        # [END print_results]

    except HttpError as err:
        print('Error: {}'.format(err.content))
        raise err


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')

    args = parser.parse_args()

    main(args.project_id)
# [END all]
