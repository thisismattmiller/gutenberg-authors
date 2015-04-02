from pyelasticsearch import ElasticSearch, exceptions
import os, json, time

class index:

	def indexLookup(self):

		es = ElasticSearch('http://104.236.54.204:9200')

		with open("author_lookup.json", "r") as f:

			lookups = json.loads(f.read())
			for lookup in lookups:

				doc = {}

				doc['id'] = lookup
					
				titles = []

				for x in lookups[lookup]:

					print (x)
					t = str(x[0]) + "|" + x[1]
					titles.append(t)

				doc['titles'] = titles





				try:
					es.index(index="titles", doc_type="title", id=lookup, doc=doc)

				except exceptions.ElasticHttpError as e:

					print("Error on this one")
					print(doc["id"])
					print(str(e))


				print (lookup)


	def indexAuthors(self):

		es = ElasticSearch('http://localhost:9200')

		with open("allData.json", "r") as f:

			authors = json.loads(f.read())

			for author in authors:

				#i don't want to add the about as a topic right now
				authors[author]['groups']['about'] = []

				print ("Doing", author)

				try:
					es.index(index="gutenberg", doc_type="author", id=authors[author]['id'], doc=authors[author])
				except exceptions.ElasticHttpError as e:


					print ("-----------------")
					print ("Error indexing this author:",author)
					print (e)
					print ("-----------------")


if __name__ == "__main__":

	b = index()

	b.indexAuthors()