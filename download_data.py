import json, os.path, requests

class Download:



	def __init__(self):

		self.startDownload()



	def startDownload(self):

		f = open("47000_metadata.json")

		for line in f:

			data = json.loads(line)


			if data['authors']:

				if len(data['authors']) > 0:

					for author in data['authors']:



						if 'wikipedia_name' in  author:

							filename = 'rdf/' + author['wikipedia_name'] + '.n3'

							print ("Working on " + author['wikipedia_name'])

							if not os.path.isfile( filename ):



								url = "http://dbpedia.org/data/" + author['wikipedia_name'] + ".n3"


								with open(filename, 'wb') as handle:
									response = requests.get(url, stream=True)

									if not response.ok:
										print ("Error:")
										print (url)

									for block in response.iter_content(1024):
										if not block:
											break

										handle.write(block)





if __name__ == "__main__":

	

	d = Download()