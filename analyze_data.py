import json, glob, rdflib, operator, requests, urllib.parse, os, unicodedata



class Analyze:

	predicates = {}

	groups =  {
	        "type" : ["http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://dbpedia.org/property/type"],
	        "about" : ["http://dbpedia.org/ontology/abstract", "http://purl.org/dc/elements/1.1/description", "http://dbpedia.org/property/shortDescription", "http://dbpedia.org/property/caption", "http://dbpedia.org/property/description"],
	        "name" : ["http://xmlns.com/foaf/0.1/name", "http://dbpedia.org/property/name", "http://xmlns.com/foaf/0.1/givenName", "http://xmlns.com/foaf/0.1/surname", "http://dbpedia.org/ontology/alias", "http://www.w3.org/2000/01/rdf-schema#label", "http://dbpedia.org/property/alternativeNames", "http://dbpedia.org/property/birthName", "http://dbpedia.org/ontology/birthName", "http://dbpedia.org/ontology/pseudonym", "http://dbpedia.org/property/pseudonym", "http://dbpedia.org/property/otherNames", "http://dbpedia.org/property/alt", "http://dbpedia.org/property/last", "http://dbpedia.org/property/first", "http://dbpedia.org/property/honorificPrefix", "http://dbpedia.org/property/honorificSuffix", "http://dbpedia.org/ontology/title"],
	        "dates" : ["http://dbpedia.org/ontology/birthDate", "http://dbpedia.org/ontology/deathDate", "http://dbpedia.org/ontology/birthYear", "http://dbpedia.org/property/dateOfBirth", "http://dbpedia.org/ontology/deathYear", "http://dbpedia.org/property/dateOfDeath", "http://dbpedia.org/property/birthDate", "http://dbpedia.org/property/deathDate", "http://dbpedia.org/property/years", "http://dbpedia.org/property/termStart", "http://dbpedia.org/property/termEnd", "http://dbpedia.org/ontology/activeYearsEndDate", "http://dbpedia.org/ontology/activeYearsStartDate", "http://dbpedia.org/ontology/activeYearsStartYear", "http://dbpedia.org/property/serviceyears", "http://dbpedia.org/ontology/serviceStartYear", "http://dbpedia.org/ontology/serviceEndYear", "http://dbpedia.org/property/yearsActive", "http://dbpedia.org/property/year", "http://dbpedia.org/ontology/era", "http://dbpedia.org/property/era", "http://dbpedia.org/ontology/activeYearsEndYear", "http://dbpedia.org/property/period", "http://dbpedia.org/property/date"],
	        "place" : ["http://dbpedia.org/property/placeOfBirth", "http://dbpedia.org/ontology/deathPlace", "http://dbpedia.org/property/birthPlace", "http://dbpedia.org/property/placeOfDeath", "http://dbpedia.org/property/deathPlace", "http://dbpedia.org/ontology/birthPlace", "http://dbpedia.org/ontology/restingPlace", "http://dbpedia.org/ontology/country", "http://dbpedia.org/property/residence", "http://dbpedia.org/property/restingPlace", "http://dbpedia.org/ontology/stateOfOrigin", "http://dbpedia.org/property/citizenship", "http://dbpedia.org/property/workplaces", "http://dbpedia.org/ontology/citizenship", "http://dbpedia.org/property/placeofburial", "http://dbpedia.org/ontology/residence", "http://dbpedia.org/property/region", "http://dbpedia.org/property/district", "http://dbpedia.org/property/restingplace", "http://dbpedia.org/property/workInstitution", "http://dbpedia.org/ontology/allegiance", "http://dbpedia.org/property/nationality", "http://dbpedia.org/ontology/nationality", "http://dbpedia.org/property/allegiance"],
	        "subject" : ["http://purl.org/dc/terms/subject", "http://www.w3.org/2004/02/skos/core#subject"],
	        "genre" : ["http://dbpedia.org/ontology/occupation", "http://dbpedia.org/property/occupation", "http://dbpedia.org/property/title", "http://dbpedia.org/ontology/genre", "http://dbpedia.org/property/movement", "http://dbpedia.org/ontology/field", "http://dbpedia.org/property/field", "http://dbpedia.org/ontology/movement", "http://dbpedia.org/property/fields", "http://dbpedia.org/ontology/philosophicalSchool", "http://dbpedia.org/ontology/profession", "http://dbpedia.org/property/subject", "http://dbpedia.org/property/genre"],
	        "people" : ["http://dbpedia.org/ontology/influenced", "http://dbpedia.org/property/influenced", "http://dbpedia.org/property/influences", "http://dbpedia.org/ontology/influencedBy", "http://dbpedia.org/property/after", "http://dbpedia.org/property/before", "http://dbpedia.org/property/spouse", "http://dbpedia.org/property/children", "http://dbpedia.org/property/successor", "http://dbpedia.org/property/predecessor", "http://dbpedia.org/ontology/child", "http://dbpedia.org/ontology/spouse", "http://dbpedia.org/property/parents", "http://dbpedia.org/property/doctoralStudents", "http://dbpedia.org/ontology/doctoralStudent", "http://dbpedia.org/property/notableStudents", "http://dbpedia.org/ontology/notableStudent", "http://dbpedia.org/ontology/relative", "http://dbpedia.org/property/succeeded", "http://dbpedia.org/property/preceded", "http://dbpedia.org/property/alongside", "http://dbpedia.org/ontology/relation", "http://dbpedia.org/property/relatives", "http://dbpedia.org/property/relations", "http://dbpedia.org/ontology/successor", "http://dbpedia.org/ontology/parent"], 
	        "works" : ["http://dbpedia.org/property/notableworks", "http://dbpedia.org/ontology/termPeriod", "http://dbpedia.org/ontology/notableIdea", "http://dbpedia.org/property/notableIdeas", "http://dbpedia.org/property/mainInterests", "http://dbpedia.org/property/notableWorks", "http://dbpedia.org/property/author", "http://dbpedia.org/property/laterwork", "http://dbpedia.org/ontology/notableWork", "http://dbpedia.org/property/knownFor", "http://dbpedia.org/ontology/knownFor", "http://dbpedia.org/ontology/mainInterest"],
	        "personal" :  ["http://dbpedia.org/ontology/almaMater", "http://dbpedia.org/ontology/religion", "http://dbpedia.org/property/quote", "http://dbpedia.org/ontology/education", "http://dbpedia.org/property/profession", "http://dbpedia.org/property/state", "http://dbpedia.org/property/align", "http://dbpedia.org/ontology/militaryCommand", "http://dbpedia.org/ontology/region", "http://dbpedia.org/property/language", "http://dbpedia.org/property/commands", "http://dbpedia.org/property/workInstitutions", "http://dbpedia.org/ontology/militaryBranch", "http://dbpedia.org/property/prizes", "http://dbpedia.org/ontology/militaryRank", "http://dbpedia.org/ontology/language", "http://dbpedia.org/property/ethnicity", "http://dbpedia.org/property/commons", "http://dbpedia.org/property/deathCause", "http://dbpedia.org/property/justice", "http://dbpedia.org/property/species", "http://dbpedia.org/ontology/office", "http://dbpedia.org/property/party", "http://dbpedia.org/ontology/party", "http://dbpedia.org/property/rank", "http://dbpedia.org/property/awards", "http://dbpedia.org/property/education", "http://dbpedia.org/property/almaMater", "http://dbpedia.org/property/branch", "http://dbpedia.org/ontology/battle", "http://dbpedia.org/property/battles", "http://dbpedia.org/ontology/award", "http://dbpedia.org/property/office", "http://dbpedia.org/property/religion"]

	}


	def __init__(self):

		#self.analyze()
		#self.buildAuthorLookup()
		#self.downloadImage()
		self.buildData()

	
	def downloadImage(self):


		files = glob.glob('./rdf/*.nt')

		for file in files:


			print ("working on " + file)

			name = file.split(".nt")[0].split("./rdf/")[1]


			with open(file) as f:
				data = f.read()


				g=rdflib.Graph()
				g.parse( data=data, format='nt' )
				for s,p,o in g:

					if str(p) == 'http://dbpedia.org/ontology/thumbnail':


						try:
							with open("images/" + name + ".jpg", 'wb') as handle:
								response = requests.get(str(o), stream=True)

								if not response.ok:
									print ("Error:")
									print (o)

								for block in response.iter_content(1024):
									if not block:
										break

									handle.write(block)

						except:
							print ("Error:")
							print (o)

	def buildData(self):


		files = glob.glob('./rdf/*.n3')
		counter = 0

		allData = {}


		with open('author_lookup.json') as f:
			author_lookup = json.loads(f.read())

		for file in files:

			counter+=1

			print ("working on " + file)

			name = file.split(".n3")[0].split("./rdf/")[1]


			allData[name] = {}


			groups =  {
			        "type" : [],
			        "about" : [],
			        "name" : [],
			        "dates" : [],
			        "place" : [],
			        "subject" : [],
			        "genre" : [],
			        "people" : [], 
			        "works" : [],
			        "personal" : [] 

			}

			if self.stripDiacritics(name) in author_lookup:

				allData[name]['titles'] = author_lookup[self.stripDiacritics(name)]

			else:

				print ("---------------")
				print ("No titles for",self.stripDiacritics(name) )
				print ("---------------")



			#check if there is an image
			if os.path.isfile('./images/' + name + '.jpg' ):
				allData[name]['image'] = True
			else:
				allData[name]['image'] = False


			rdf = {}

			with open(file, encoding='utf-8') as f:
				data = f.read()

				try:

					g=rdflib.Graph()
					g.parse( data=data, format='n3' )
					for s,p,o in g:


						for aGroup in self.groups:

							if str(p) in self.groups[aGroup]:


								#store the lang in the about strings since we are using
								#eleastic search as our storage too
								if hasattr(o, 'language'):
									
									lang = ""

									if aGroup == 'about':
										if o.language != None:
											lang = "@" + o.language

									value = lang + str(o)
								else:
									value = str(o)




								if value.find("http://") > -1:

									if value.find("yago") > -1:
										continue


									value = value.split("/")
									value = value[len(value) -1]

									value = value.replace('Category:','')
									value = value.replace('_',' ')

									value = urllib.parse.unquote(value)

									#print (value)


								if aGroup == "dates" and value.find("+") > -1:
									value = value.split("+")[0]


								if aGroup == "dates" and value.find("--") > -1:
									continue


								if value not in groups[aGroup]:

									groups[aGroup].append(value)

									if str(p) not in rdf:
										rdf[str(p)] = []

									rdf[str(p)].append(value)




				except Exception as e:

					print ("------------------")
					print ("Error with\n",file)
					print (e)
					print ("------------------")



			allData[name]['groups'] = groups
			allData[name]['rdf'] = rdf
			allData[name]['id'] = name

		with open('allData.json', 'w') as f:
			f.write(json.dumps(allData,indent=2,sort_keys=False))



	def buildAuthorLookup(self):

		authors = {}


		f = open("47000_metadata.json")

		for line in f:

			data = json.loads(line)


			if data['authors']:

				if len(data['authors']) > 0:

					for author in data['authors']:



						if 'wikipedia_name' in  author:

							sanDiacritics = self.stripDiacritics(author['wikipedia_name'])


							print ("Working on " + sanDiacritics)


							if sanDiacritics not in authors:

								authors[sanDiacritics] = []

							authors[sanDiacritics].append( [ data['gutenberg_id'], data['title']   ]  )





		#sortedPredicates = sorted(self.predicates.items(), key=operator.itemgetter(1), reverse=True)
		with open('author_lookup.json', 'w') as f:
			f.write(json.dumps(authors,sort_keys=False))

	def analyze(self):

		files = glob.glob('./rdf/*.nt')
		counter = 0

		for file in files:

			counter+=1

			print ("working on " + file)

			with open(file) as f:
				data = f.read()

				try:

					g=rdflib.Graph()
					g.parse( data=data, format='nt' )
					for s,p,o in g:

						if str(p) not in self.predicates:
							self.predicates[str(p)] = 1
						else:
							self.predicates[str(p)] += 1


				except rdflib.plugins.parsers.ntriples.ParseError:

					print ("Error with\n",file)

				#if counter > 1000:
				#	break


		sortedPredicates = sorted(self.predicates.items(), key=operator.itemgetter(1), reverse=True)

		with open('sorted_predicates.json', 'w') as f:
			f.write(json.dumps(sortedPredicates,indent=4,sort_keys=False))


	def stripDiacritics(self,s):

		return ''.join(c for c in unicodedata.normalize('NFD', s)
			if unicodedata.category(c) != 'Mn')

if __name__ == "__main__":

	

	d = Analyze()