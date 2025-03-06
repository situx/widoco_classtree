import os
import argparse


classtreejs="""
function generateClassTree(titleattarr, superatt, classOrProp) {
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
    var topConcept="#"
    if (titleattarr.includes("class")) {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#Thing",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
            "parent": "#",
            "text": "owl:Thing"
        })
        parentmap["http://www.w3.org/2002/07/owl#Thing"]=true
        topConcept="http://www.w3.org/2002/07/owl#Thing"
    } else if (titleattarr.includes("data property") || titleattarr.includes("datatype property")) {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#topDataProperty",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
            "parent": "#",
            "text": "owl:topDataProperty"
        })
        parentmap["http://www.w3.org/2002/07/owl#topDataProperty"]=true
        topConcept="http://www.w3.org/2002/07/owl#topDataProperty"
    } else if (titleattarr.includes("annotation property")) {
        topConcept="#"
    }else if (titleattarr.includes("named individual")) {
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
    for(titleatt of titleattarr){
    $('#ontview').contents().find(' h3 > sup[title="' + titleatt + '"]').each(function() {
        //console.log($(this))
        if (counter > 0) {
            var id = $(this).parent().parent().attr("id");
            //console.log(id)
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

            //console.log("Superclasses")
            if (!(id.startsWith("4"))) {
                sup = $(this).parent().parent().children('dl').children('dt:contains("' + superatt + '")').next().children("a")
                //console.log("Sup: ")
                //console.log(sup)
                if (sup.length != 0) {
                    sup.each(function() {
                        //console.log($(this))
                        theth=$(this).parent().parent().children("table").children("tbody").children("tr").children("th")
                        uri=$(theth[0]).next().children("code")
                        console.log("URI Elem: ")
                        console.log(uri)
                        if(typeof(uri)!=='undefined'){
                            console.log("URI: ")
                            console.log(uri.html())
                            if(uri.html().startsWith("http")){
                                id=uri.html()
                            }                  
                        }
                        
                        //console.log(theth)
                        if(titleatt=="class" && typeof(theth)!=='undefined' && typeof($(theth).next().children("a").attr("href"))!=='undefined'){
                            //console.log($(theth).next().children("a").attr("href"))
                            parentcls=$(theth).next().children("a").attr("href")
                        }else if (!($(this).attr("href").startsWith("4"))) {
                            parentcls = $(this).attr("href")
                            //console.log($(this).attr("href"));
                        }
                    });
                } else {
                    theth=$(this).parent().parent().children("table").children("tbody").children("tr").children("th")
                    if(titleatt=="class" && typeof(theth)!=='undefined'){
                        //console.log(theth[2])
                        //console.log($(theth[2]).next().children("a").attr("href"))
                        uri=$(theth[0]).next().children("code")
                        console.log("URI Elem: ")
                        console.log(uri)
                        if(typeof(uri)!=='undefined'){
                            console.log("URI: ")
                            console.log(uri.html())
                            if(uri.html().startsWith("http")){
                                id=uri.html()
                            }                  
                        }
                        theth=$(theth[2]).next().children("a")                        
                        theth.each(function() {        
                            //console.log($(this).attr("href"))
                            parentcls = $(this).attr("href")
                        });
                    }else{
                       $(this).parent().parent().children('div').children('dl').children('dt:contains("' + superatt + '")').next().children("a").each(function() {
                        //console.log($(this))
                        if (!($(this).attr("href").startsWith("4"))) {
                            parentcls = $(this).attr("href")
                            //console.log($(this).attr("href"));
                        }
                    });
                    }

                }
                //console.log(parentcls)
                
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
                    if (id != "http://www.w3.org/2002/07/owl#Thing" && id!="#"){
                       if (!(parentcls in parentmap) && parentcls!="#") {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            treeitem={
                                "id": parentcls,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt2
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[parentcls] = treeitem
                       }
                       if(id==parentcls){
                           treeitem={
                                "id": id,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt
                            }
                           classTree["core"]["data"].push(treeitem)
                           parentmap[id] = treeitem
                       }else{
                           treeitem={
                                "id": id,
                                "parent": parentcls,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt
                            }
                           classTree["core"]["data"].push(treeitem)
                           parentmap[id] = treeitem
                       }
                       
                    }
                } else if (titleatt == "data property" || titleatt == "datatype property") {
                    if (id != "http://www.w3.org/2002/07/owl#topDataProperty" && id!="#"){
                        if (!(parentcls in parentmap) && parentcls!="#") {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            treeitem={
                                "id": parentcls,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
                                "text": textt2
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[parentcls] = treeitem
                        }
                        if(id==parentcls){
                            treeitem={
                                "id": id,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id] = treeitem
                        }else{
                            treeitem={
                                "id": id,
                                "parent": parentcls,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id] = treeitem
                        }
                        
                    }
                } else if (titleatt == "annotation property") {
                        classTree["core"]["data"].push({
                            "id": id,
                            "parent": "#",
                            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Metadata.gif",
                            "text": textt
                        })                        
                }else if (titleatt == "named individual") {
                    if (id != "http://www.w3.org/2002/07/owl#NamedIndividual" && id!="#"){
                        if (!(parentcls in parentmap) && parentcls!="#") {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            treeitem={
                                "id": parentcls,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt2
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[parentcls] = treeitem
                        }
                        if(id==parentcls){
                            treeitem={
                                "id": id,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id] = treeitem
                        }else{
                            treeitem={
                                "id": id,
                                "parent": parentcls,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id] = treeitem
                        }
                        
                    }
                } else {
                    if (id != "http://www.w3.org/2002/07/owl#topObjectProperty" && id!="#"){
                       if (!(parentcls in parentmap) && parentcls!="#") {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                           treeitem={
                                "id": parentcls,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
                                "text": textt2
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[parentcls] = treeitem
                        }
                        if(id==parentcls){
                            treeitem={
                                "id": id,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id]=treeitem
                        }else if(id in parentmap && parentmap[id]["parent"]==topConcept){
                            parentmap[id]["parent"]=parentcls
                        }else{
                            treeitem={
                                "id": id,
                                "parent": parentcls,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)  
                            parentmap[id]=treeitem
                        }
                        //parentmap[id] = true
                    }
                }


            }
        }
        counter++;
    });
    }
    console.log(classTree["core"]["data"])
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
"""

htmltemplate="""
<html>
<head>
<title>Widoco Classtree</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.9/jstree.min.js"></script>
<script type="text/javascript" src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.bundle.min.js"></script>
	<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"/>
	<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"/>
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css" />
 <style>
 html {
    position: relative;
    min-height: 100%;
}
.fill { 
	max-height: 95%;
    min-height: 95%;
    height: 95%;
}
</style>
</head>
<body>
<header id="header">
<h1 align="center">{{pagetitle}}</h1>
</header>
<div class="container-fluid fill" role="main"><div class="row fill">
<div class="col-sm-4 fill">
Search Classes: <input id="search-input" class="search-input" />
<br /><fieldset id="classesinds"><input id="classes" type="radio" name="classesinds" checked="checked"/>Classes&nbsp;<input type="radio" name="classesinds" id="individuals"/>Individuals</fieldset><br/>
<div id="jstree_demo_div" class="overflow-auto" style="height:44%">Loading tree...</div>
<div id="jstree_demo_div1" class="overflow-auto" style="height:44%;display:none" >Loading tree...</div>
<hr/>
Search Properties: <input id="search-input2" class="search-input" />
<br />
<fieldset id="properties">
<input id="objprop" name="properties" type="radio" checked="checked"/>ObjectProperties&nbsp;<input type="radio" name="properties" id="dataprop"/>DatatypeProperties<!--&nbsp;<input name="properties" type="radio" id="annoprop"/>AnnotationProperties--></fieldset><br/>
<div id="jstree_demo_div2" class="overflow-auto" style="height:44%" style="visibility:hidden">Loading tree...</div>
<div id="jstree_demo_div3" class="overflow-auto" style="height:44%;display:none">Loading tree...</div>
<div id="jstree_demo_div4" class="overflow-auto" style="height:44%;display:none">Loading tree...</div>
</div>
<div class="col-sm-8" style="min-height:100%;height:100%">
<iframe width="100%" height="100%" id="ontview" src="{{docfile}}">
</iframe>
</div></div></div>
<!--
<button onClick="genclassTree()">
Generate Class Tree</button>-->
<footer id="footer">
</footer>
</body>
<script src="classtree.js"></script>
<script>
function goToId(id) {
    if(id.includes("#")){
		var iframe = document.getElementById("ontview").contentWindow.location.hash=id.substring(id.lastIndexOf('#')+1);
	}else if(id.startsWith("http")){
		var iframe = document.getElementById("ontview").contentWindow.location.hash=id.substring(id.lastIndexOf('/')+1);
	}else{
		var iframe = document.getElementById("ontview").contentWindow.location.hash=id;
	}
}
function genclassTree(){
	$('#jstree_demo_div').jstree(generateClassTree(["class"],"has super-classes",true));
	$('#jstree_demo_div1').jstree(generateClassTree(["named individual"],"belongs to",false));
	$('#jstree_demo_div2').jstree(generateClassTree(["object property"],"has super-properties",false));
	$('#jstree_demo_div3').jstree(generateClassTree(["data property","datatype property"],"has super-properties",false));
	//$('#jstree_demo_div4').jstree(generateClassTree(["annotation property"],""));
	$('#annoprop').click(function() {
        $('#jstree_demo_div2').hide();
        $('#jstree_demo_div3').hide();
        $('#jstree_demo_div4').show();
        $( "#search-input2").unbind( "keyup" );
        $("#search-input2").keyup(function () {
            var searchString = $(this).val();
            $('#jstree_demo_div4').jstree('search', searchString);
        });
    });
    $('#dataprop').click(function() {
        $('#jstree_demo_div2').hide();
        $('#jstree_demo_div3').show();
        $('#jstree_demo_div4').hide();
        $( "#search-input2").unbind( "keyup" );
        $("#search-input2").keyup(function () {
            var searchString = $(this).val();
            $('#jstree_demo_div3').jstree('search', searchString);
        });
    });
    $('#objprop').click(function() {
        $('#jstree_demo_div2').show();
        $('#jstree_demo_div3').hide();
        $('#jstree_demo_div4').hide();
        $( "#search-input2").unbind( "keyup" );
        $("#search-input2").keyup(function () {
            var searchString = $(this).val();
            $('#jstree_demo_div2').jstree('search', searchString);
        });
    });
    $('#classes').click(function() {
        $('#jstree_demo_div').show();
        $('#jstree_demo_div1').hide();
        $( "#search-input").unbind( "keyup" );
        $("#search-input").keyup(function () {
            var searchString = $(this).val();
            $('#jstree_demo_div').jstree('search', searchString);
        });
    });
    $('#individuals').click(function() {
        $('#jstree_demo_div').hide();
        $('#jstree_demo_div1').show();
        $( "#search-input").unbind( "keyup" );
        $("#search-input").keyup(function () {
            var searchString = $(this).val();
            $('#jstree_demo_div1').jstree('search', searchString);
        });
    });
    $("#jstree_demo_div").on(
        "select_node.jstree", function(evt, data){
			//console.log(data)
			//console.log(data.node.id)
			goToId(data.node.id)
            //selected node object: data.node;
        }
	);
	$("#jstree_demo_div1").on(
        "select_node.jstree", function(evt, data){
			//console.log(data)
			//console.log(data.node.id)
			goToId(data.node.id)
            //selected node object: data.node;
        }
	);
	$("#jstree_demo_div2").on(
        "select_node.jstree", function(evt, data){
			//console.log(data)
			//console.log(data.node.id)
			goToId(data.node.id)
            //selected node object: data.node;
        }
	);
		$("#jstree_demo_div3").on(
        "select_node.jstree", function(evt, data){
			//console.log(data)
			//console.log(data.node.id)
			goToId(data.node.id)
            //selected node object: data.node;
        }
	);
		$("#jstree_demo_div4").on(
        "select_node.jstree", function(evt, data){
			//console.log(data)
			//console.log(data.node.id)
			goToId(data.node.id)
            //selected node object: data.node;
        }
	);
}
$('#ontview').on('load', function(){genclassTree()});
 $("#search-input").keyup(function () {
      var searchString = $(this).val();
     $('#jstree_demo_div').jstree('search', searchString);
 });
  $("#search-input2").keyup(function () {
      var searchString = $(this).val();
     $('#jstree_demo_div2').jstree('search', searchString);
 });
</script>
</html>"""


parser=argparse.ArgumentParser()
parser.add_argument("-i","--input",nargs='?',help="the HTML doc file to parse",action="store",required=True)
parser.add_argument("-o","--output",nargs='?',help="the name of the new HTML doc file",action="store",required=True,default="content.html")
parser.add_argument("-t","--title",nargs='?',help="the title to show in the HTML page",action="store",required=False,default="OntologyView")
args, unknown=parser.parse_known_args()

file_path = args.input
print(file_path)

with open(file_path, 'r',encoding="utf-8") as file:
    htmlpage = file.read()

with open(args.output,'w',encoding="utf-8") as file:
    file.write(htmlpage)

jspath=args.output
if "/" in str(args.output):
    jspath=args.output[args.output.rfind("/")]
else:
    jspath=""
jspath+="classtree.js"
with open(jspath,'w',encoding="utf-8") as file:
    file.write(classtreejs)
    
with open(file_path,'w',encoding="utf-8") as file:
    file.write(htmltemplate.replace("{{docfile}}",str(args.output)).replace("{{pagetitle}}",args.title))
    
