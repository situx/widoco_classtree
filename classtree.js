function generateClassTree(titleatt, superatt, classOrProp) {
    classTree = {
        "plugins": ["search", "types", "sort", "state", "wholerow"],
        "search": {
            "case_sensitive": false,
            "show_only_matches": true
        },
        "core": {
            "data": []
        }
    }
    parentmap = {}
    var topConcept=""
    if (titleatt == "class") {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#Thing",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
            "parent": "#",
            "text": "owl:Thing"
        })
         parentmap["http://www.w3.org/2002/07/owl#Thing"]=true
        topConcept="http://www.w3.org/2002/07/owl#Thing"
    } else if (titleatt == "data property") {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#topDataProperty",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
            "parent": "#",
            "text": "owl:topDataProperty"
        })
        parentmap["http://www.w3.org/2002/07/owl#topDataProperty"]=true
        topConcept="http://www.w3.org/2002/07/owl#topDataProperty"
    } else if (titleatt == "named individual") {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#NamedIndividual",
            "parent": "#",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
            "text": "owl:NamedIndividual"
        })
        parentmap["http://www.w3.org/2002/07/owl#NamedIndividual"]=true
        topConcept="http://www.w3.org/2002/07/owl#NamedIndividual"
    } else {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#topObjectProperty",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
            "parent": "#",
            "text": "owl:topObjectProperty"
        })
        parentmap["http://www.w3.org/2002/07/owl#topObjectProperty"]=true
        topConcept="http://www.w3.org/2002/07/owl#topObjectProperty"
    }

    var counter = 0;
    //console.log($('#ontview').contents())
    //console.log($('#ontview').contents().find('.type-c'))
    //console.log($('#ontview').contents().find(' h3 > sup[title="'+titleatt+'"]'))
    $('#ontview').contents().find(' h3 > sup[title="' + titleatt + '"]').each(function() {
        console.log($(this))
        if (counter > 0) {
            var id = $(this).parent().parent().attr("id");
            console.log(id)
            var parentcls = "";
            if (titleatt == "class") {
                parentcls = "http://www.w3.org/2002/07/owl#Thing"
            } else if (titleatt == "data property") {
                parentcls = "http://www.w3.org/2002/07/owl#topDataProperty"
            } else if (titleatt == "object property") {
                parentcls = "http://www.w3.org/2002/07/owl#topObjectProperty"
            } else if (titleatt == "named individual") {
                parentcls = "http://www.w3.org/2002/07/owl#NamedIndividual"
            }

            console.log("Superclasses")
            if (!(id.startsWith("4"))) {
                sup = $(this).parent().parent().children('dl').children('dt:contains("' + superatt + '")').next().children("a")
                console.log("Sup: ")
                console.log(sup)
                /*console.log($(this).parent().parent())
                console.log($(this).parent().parent().children("table"))
                console.log($(this).parent().parent().children("table").children("tbody").children("tr").children("th"))
                console.log($(this).parent().parent().children("table").children("tbody").children("tr").children("th").next().children("a"))
                console.log($(this).parent().parent().children("table").children("tbody").children("tr").children("th").next().children("a").attr("href"))
                theth=$(this).parent().parent().children("table").children("tbody").children("tr").children("th")[2]
                console.log(theth)
                console.log($(theth).next().children("a").attr("href"))*/
                if (sup.length != 0) {
                    sup.each(function() {
                        //console.log($(this))
                        
                        console.log(theth)
                        if(titleatt=="class" && typeof(theth)!=='undefined'){
                            console.log($(theth).next().children("a").attr("href"))
                            parentcls=$(theth).next().children("a").attr("href").substring($(theth).next().children("a").attr("href").indexOf('#') + 1)
                        }else if (!($(this).attr("href").startsWith("4"))) {
                            parentcls = $(this).attr("href").substring($(this).attr("href").indexOf('#') + 1)
                            //console.log($(this).attr("href"));
                        }
                    });
                } else {
                    theth=$(this).parent().parent().children("table").children("tbody").children("tr").children("th")
                    if(titleatt=="class" && typeof(theth)!=='undefined'){
                        console.log(theth[2])
                        console.log($(theth[2]).next().children("a").attr("href"))
                        theth=$(theth[2]).next().children("a")                        
                        theth.each(function() {        
                        console.log($(this).attr("href"))
                        parentcls = $(this).attr("href")
                        });
                    }else{
                       $(this).parent().parent().children('div').children('dl').children('dt:contains("' + superatt + '")').next().children("a").each(function() {
                        //console.log($(this))
                        if (!($(this).attr("href").startsWith("4"))) {
                            parentcls = $(this).attr("href").substring($(this).attr("href").indexOf('#') + 1)
                            //console.log($(this).attr("href"));
                        }
                    });
                    }

                }
                console.log(parentcls)
                
                if (parentcls == "") {
                    parentcls = "#"
                }

                ////console.log(superclasslist[0])
                //var topush={ "id" : id,parent:
                if (id.includes('#')) {
                    var textt = id.substring(id.lastIndexOf('#') + 1)
                } else {
                    var textt = id.substring(id.lastIndexOf('/') + 1)
                }
                if (titleatt == "class") {
                    if (id != "http://www.w3.org/2002/07/owl#Thing"){
                       if (!(parentcls in parentmap)) {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            classTree["core"]["data"].push({
                                "id": parentcls,
                                "parent": "#",
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt2
                            })
                            parentmap[parentcls] = true
                       }
                       classTree["core"]["data"].push({
                            "id": id,
                            "parent": parentcls,
                            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                            "text": textt
                        })
                    }
                } else if (titleatt == "data property") {
                    if (id != "http://www.w3.org/2002/07/owl#topDataProperty"){
                        if (!(parentcls in parentmap)) {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            classTree["core"]["data"].push({
                                "id": parentcls,
                                "parent": "#",
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
                                "text": textt2
                            })
                            parentmap[parentcls] = true
                        }
                        classTree["core"]["data"].push({
                            "id": id,
                            "parent": parentcls,
                            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
                            "text": textt
                        })
                    }
                } else if (titleatt == "named individual") {
                    if (id != "http://www.w3.org/2002/07/owl#NamedIndividual"){
                        if (!(parentcls in parentmap)) {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            classTree["core"]["data"].push({
                                "id": parentcls,
                                "parent": "#",
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt2
                            })
                            parentmap[parentcls] = true
                        }
                        classTree["core"]["data"].push({
                            "id": id,
                            "parent": parentcls,
                            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif",
                            "text": textt
                        })
                    }
                } else {
                    if (id != "http://www.w3.org/2002/07/owl#topObjectProperty"){
                       if (!(parentcls in parentmap)) {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            classTree["core"]["data"].push({
                                "id": parentcls,
                                "parent": "#",
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
                                "text": textt2
                            })
                            parentmap[parentcls] = true
                        }
                        classTree["core"]["data"].push({
                            "id": id,
                            "parent": parentcls,
                            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
                            "text": textt
                        })
                    }
                }

                console.log(classTree["core"]["data"])
            }
        }
        counter++;

    });
    //console.log(classTree)
    return classTree;
}

function createClassTreeFromJSON(json) {
    classTree = {
        "plugins": ["search", "types", "sort", "state", "wholerow"],
        "search": {
            "case_sensitive": false,
            "show_only_matches": true
        },
        "core": {
            "data": []
        }
    }
    classTree["core"]["data"] = json
    return classTree
}
