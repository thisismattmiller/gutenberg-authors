

var gutenberg = {

	abstractsEng : {},
	abstractAll : {},


	init: function(){

		var self =this;


		var typeaheadQueryThrottled = _.throttle(self.typeaheadQuery, 700);


		var suggestionTemplate = _.template($("#template-typeahead-suggestion").html());
		var noResultsTemplate = _.template($("#template-typeahead-noresult").html());


		//initalize the typeahead box
		$('#search-box').typeahead(null, {
		  name: 'author',
		  displayKey: 'value',
		  source: typeaheadQueryThrottled,

		  templates: {



		  		suggestion : suggestionTemplate,
		  		empty: noResultsTemplate

		  }


		});



		$('#search-box').on("typeahead:selected",this.execute);

		$('#search-box-form').on('submit', this.execute);

		$("#example-links a").click(function(event){

			$("#search-box").val($(this).text());
			self.execute(event);

		});

		$(window).resize(function(){

			$(".tt-dropdown-menu").css("width",$(".twitter-typeahead").width() + "px");


		});

		$(window).resize();

	},

	execute: function(event,suggestion,dataset){

		$('#search-box').typeahead('close');

		//if they submited the form we need the value
		if (!suggestion) var suggestion = { value: $("#search-box").val()};



		var q = {

			"query": {
				"multi_match": {
					"query":	suggestion.value,
					"fields":   [ "groups.*.autocomplete" ]
				}
			},
		    "highlight" : {
		        "fields" : {
		            "groups.*.autocomplete"    : {}
		        }
		    }

		}



		var resultTemplate = _.template($("#template-result").html());

		$("#results").empty().html("<h1>Loading...</h1>");


		$.post( "http://104.131.6.35/gutenberg/author/_search/", JSON.stringify(q), function(data) {


			$("#results").empty();

			for (var index in data.hits.hits){

				var hit = data.hits.hits[index]._source;
				var highlight = data.hits.hits[index].highlight;

				var image = (hit.image) ? '<img class="author-img" id="author-img-'+index+'" src="img_authors/' + hit.id + '.jpg">' : '<img class="author-img" style="opacity:0.5" src="img/no_img.png"/>';
				var name = (hit.rdf['http://dbpedia.org/property/name']) ? hit.rdf['http://dbpedia.org/property/name'][0] : hit.id.replace(/_/g," ");

				var abstractEng = "No Engligh abstract available."
				var abstractAll = {}


				for (var x in hit.rdf['http://dbpedia.org/ontology/abstract']){

					if (hit.rdf['http://dbpedia.org/ontology/abstract'][x].substring(0,3) == "@en"){
						abstractEng = hit.rdf['http://dbpedia.org/ontology/abstract'][x].substring(3,hit.rdf['http://dbpedia.org/ontology/abstract'][x].length-1);
						abstractAll['en'] = abstractEng;

						gutenberg.abstractsEng[index] = abstractEng;
					}else{
						abstractAll[hit.rdf['http://dbpedia.org/ontology/abstract'][x].substring(1,3)] = hit.rdf['http://dbpedia.org/ontology/abstract'][x].substring(3,hit.rdf['http://dbpedia.org/ontology/abstract'][x].length-1);
					}


				}

				gutenberg.abstractAll[index] = abstractAll;

				var valueIndex = {

					"about" 	: {"hits":[],"noHits":[]},
					"dates" 	: {"hits":[],"noHits":[]},
					"genre" 	: {"hits":[],"noHits":[]},
					"name" 		: {"hits":[],"noHits":[]},
					"people" 	: {"hits":[],"noHits":[]},
					"personal" 	: {"hits":[],"noHits":[]},
					"place" 	: {"hits":[],"noHits":[]},
					"subject" 	: {"hits":[],"noHits":[]},
					"type" 		: {"hits":[],"noHits":[]},
					"works" 	: {"hits":[],"noHits":[]}
				};			

				for (var x in hit['groups']){

					var aGroup = hit['groups'][x];

					if (aGroup.length>0){

						//first add in all the items in this group
						for (var y in aGroup){

							var i = aGroup[y];

							//if it is a perfect match then it won't be hlighlited but we want it to be
							if (i == suggestion.value){
								i = "<mark>"+i+"</mark>";		
								valueIndex[x]['hits'].push(i);
							}else{
								valueIndex[x]['noHits'].push(i);
							} 					

							

						}

						if (highlight){

							if (highlight['groups.'+x+'.autocomplete']){
								
								//loop through all the highlight results
								for (var y in highlight['groups.'+x+'.autocomplete']){

									//get the highltight value, the string with html markup
									var h = highlight['groups.'+x+'.autocomplete'][y];

									//remove the markup and look for it in the lookup
									var hIndex = valueIndex[x]['noHits'].indexOf(h.replace("<em>","").replace("</em>",""))

									if (hIndex>-1){
										//it was a hit add it to the hits and remove it from the nonhits
										valueIndex[x]['noHits'].splice(hIndex, 1);
										valueIndex[x]['hits'].unshift(h.replace(/em>/gi,"mark>"));
									}


								}



							}
						}

					}

				}



				$("#results").append( resultTemplate({ index:index, titles: hit.titles, valueIndex:valueIndex, image: image, name:name, abstractEng: abstractEng, abstractAll : abstractAll })  );

				$("#author-img-"+index).error(function(){
					$(this).css("display","none");
					$(this).parent().append('<img class="author-img" style="opacity:0.5" src="img/no_img.png"/>')
				});

				$("#expand-"+index).click(function(event){
					$("#abstract-"+$(this).data("index")).text(gutenberg.abstractsEng[$(this).data("index")]);
					$(this).remove();
					event.preventDefault();
					return false;
				});


				$("#expand-subjects-"+index+","+"#expand-place-"+index+","+"#expand-genre-"+index+","+"#expand-type-"+index+","+"#expand-place-"+index+","+"#expand-people-"+index+","+"#expand-personal-"+index).click(function(event){
					$(this).siblings().first().css("display","block");
					$(this).parent().css("margin-left",0);
					event.preventDefault();
					$(this).remove();
					return false;
				})



				$("#language-"+index).change(function(event){

					
					$("#abstract-"+$(this).data("index")).text(gutenberg.abstractAll[$(this).data("index")][$(this).val()]);

					$("#expand-"+$(this).data("index")).remove();

					$('html, body').animate({scrollTop: $("#abstract-"+$(this).data("index")).offset().top-50}, 500);

					event.preventDefault();
					return false;
				})


			}

		})
		.fail(function() {
			
			alert("Errror")

		});




		//prevent the form submission
		event.preventDefault();
		return false;

	},

	//function that recives typeahead input and quries the server
	typeaheadQuery: function(query, cb){




		if (query.length<3) { return false};

		var results = [];

		var q = {

			"fields" : ["highlight"],
			"query": {
				"multi_match": {
					"query":	query,
					"fields":   [ "groups.*.autocomplete" ]
				}
			},
		    "highlight" : {
		        "fields" : {
		            "groups.*.autocomplete"    : {}
		        }
		    }

		}




		$.post( "http://104.131.6.35/gutenberg/author/_search/", JSON.stringify(q), function(data) {

			var valueIndex = {

				"groups.about.autocomplete" : {},
				"groups.dates.autocomplete" : {},
				"groups.genre.autocomplete" : {},
				"groups.people.autocomplete" : {},
				"groups.personal.autocomplete" : {},
				"groups.place.autocomplete" : {},
				"groups.subject.autocomplete" : {},
				"groups.type.autocomplete" : {},
				"groups.works.autocomplete" : {}

			};
			var tooltip = {

				"groups.about.autocomplete" : "About",
				"groups.dates.autocomplete" : "Dates",
				"groups.genre.autocomplete" : "Genre",
				"groups.people.autocomplete" : "People",
				"groups.personal.autocomplete" : "Personal Facts",
				"groups.place.autocomplete" : "Place",
				"groups.subject.autocomplete" : "Subject",
				"groups.type.autocomplete" : "Entity Type",
				"groups.works.autocomplete" : "Works"

			}			

			//response looks like this:
			// {
			//     "_shards": {
			//         "failed": 0,
			//         "successful": 5,
			//         "total": 5
			//     },
			//     "hits": {
			//         "hits": [
			//             {
			//                 "_id": "Mary_Hays",
			//                 "_index": "gutenberg",
			//                 "_score": 2.8174973,
			//                 "_type": "author",
			//                 "highlight": {
			//                     "groups.genre.autocomplete": [
			//                         "writer, <em>feminist</em>"
			//                     ],
			//                     "groups.subject.autocomplete": [
			//                         "<em>Feminism</em> and history",
			//                         "<em>Feminist</em> writers"
			//                     ],
			//                     "groups.works.autocomplete": [
			//                         "compiling and editing <em>Female</em> Biography"
			//                     ]
			//                 }
			//             }]
			//         }
			//     }
			// }


			for (var index in data.hits.hits){
				
				var d = data.hits.hits[index].highlight;				

				for (var key in d){

					for (var anItem in d[key]){


						//do we have this value for this type yet?

						if (valueIndex[key][d[key][anItem]]){
							valueIndex[key][d[key][anItem]]++;
						}else{
							valueIndex[key][d[key][anItem]]=1;
							results.push({

								display : d[key][anItem].replace(/(\r\n|\n|\r)/gm,"").replace(/<em>/gi, '<mark>').replace(/<\/em>/gi, '</mark>') ,
								value   : d[key][anItem].replace(/(\r\n|\n|\r)/gm,"").replace(/<em>/gi, '').replace(/<\/em>/gi, ''),	
								type    : key.replace('groups.','').replace('.autocomplete',''),
								tooltip : tooltip[key]

							});

						}

					}




				}

			}

			cb(results)



		})
		.fail(function() {
			cb(false)
		});


	},



}






$(document).ready(function(){


	gutenberg.init()

});
