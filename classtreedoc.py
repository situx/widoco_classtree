import os
import argparse


classtreejs="""
function generateClassTree(titleatt,superatt,classOrProp){
	classTree={"plugins": ["search", "types","sort","state","wholerow"],"search": {"case_sensitive": false,"show_only_matches": true}, "core": { "data" :[]}}
    parentmap={}
    if(titleatt=="class"){
	    classTree["core"]["data"].push({ "id" : "http://www.w3.org/2002/07/owl#Thing", "icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif", "parent":"#", "text" : "owl:Thing" })
    }else if(titleatt=="data property"){
		classTree["core"]["data"].push({ "id" : "http://www.w3.org/2002/07/owl#topDataProperty", "icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif", "parent":"#", "text" : "owl:topDataProperty" })
    }else if(titleatt=="named individual"){
		classTree["core"]["data"].push({ "id" : "http://www.w3.org/2002/07/owl#NamedIndividual", "parent":"#", "icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif", "text" : "owl:NamedIndividual" })
	}else{
		classTree["core"]["data"].push({ "id" : "http://www.w3.org/2002/07/owl#topObjectProperty", "icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif", "parent":"#", "text" : "owl:topObjectProperty" })
	}
	var counter=0;
	//console.log($('#ontview').contents())
	//console.log($('#ontview').contents().find('.type-c'))
	//console.log($('#ontview').contents().find(' h3 > sup[title="'+titleatt+'"]'))
	$('#ontview').contents().find(' h3 > sup[title="'+titleatt+'"]').each(function() {
		console.log($(this))
		if(counter>0){
		var id=$(this).parent().parent().attr("id");
		////console.log(id)
        var parentcls="";
        if(titleatt=="class"){
            parentcls="http://www.w3.org/2002/07/owl#Thing"
	    }else if(titleatt=="data property"){
            parentcls="http://www.w3.org/2002/07/owl#topDataProperty"
		}else if(titleatt=="object property"){
		    parentcls="http://www.w3.org/2002/07/owl#topObjectProperty"
		}else if(titleatt=="named individual"){
		    parentcls="http://www.w3.org/2002/07/owl#NamedIndividual"
		}

		////console.log("Superclasses")
		if(!(id.startsWith("4"))){
			sup=$(this).parent().parent().children('dl').children('dt:contains("'+superatt+'")').next().children("a")
			if(sup.length!=0){
			$(this).parent().parent().children('dl').children('dt:contains("'+superatt+'")').next().children("a").each(function(){
			//console.log($(this))
			if(!($(this).attr("href").startsWith("4"))){
				parentcls=$(this).attr("href").substring($(this).attr("href").indexOf('#')+1)
				//console.log($(this).attr("href"));
			}
		});
			}else{
					$(this).parent().parent().children('div').children('dl').children('dt:contains("'+superatt+'")').next().children("a").each(function(){
			//console.log($(this))
			if(!($(this).attr("href").startsWith("4"))){
				parentcls=$(this).attr("href").substring($(this).attr("href").indexOf('#')+1)
				//console.log($(this).attr("href"));
			}
		});
			}

		if(parentcls==""){
			parentcls="#"
		}
		
		////console.log(superclasslist[0])
		//var topush={ "id" : id,parent:
		if(id.includes('#')){
			var textt=id.substring(id.lastIndexOf('#')+1)
		}else{
			var textt=id.substring(id.lastIndexOf('/')+1)
		}
		if(titleatt=="class"){
			if(id!="http://www.w3.org/2002/07/owl#Thing")
				classTree["core"]["data"].push({ "id" : id, "parent":parentcls,"icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif", "text" : textt })
        }else if(titleatt=="data property"){
			if(id!="http://www.w3.org/2002/07/owl#topDataProperty")
				classTree["core"]["data"].push({ "id" : id, "parent":parentcls,"icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif", "text" : textt })
		}else if(titleatt=="named individual"){
		     if(!(parentcls in parentmap)){
				if(parentcls.includes('#')){
					var textt2=parentcls.substring(parentcls.lastIndexOf('#')+1)
				}else{
					var textt2=parentcls.substring(parentcls.lastIndexOf('/')+1)
				}
		        classTree["core"]["data"].push({ "id" : parentcls, "parent":"#","icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif", "text" : textt2 })
		        parentmap[parentcls]=true
		    }
			classTree["core"]["data"].push({ "id" : id, "parent":parentcls,"icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif", "text" : textt })
		}else{
			if(id!="http://www.w3.org/2002/07/owl#topObjectProperty")
				classTree["core"]["data"].push({ "id" : id, "parent":parentcls,"icon" : "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif", "text" : textt })
        }
		
		console.log(classTree["core"]["data"])
		}
		}
		counter++;
		
	});
	//console.log(classTree)
	return classTree;
}

function createClassTreeFromJSON(json){
	classTree={"plugins": ["search", "types","sort","state","wholerow"],"search": {"case_sensitive": false,"show_only_matches": true}, "core": { "data" :[]}}
	classTree["core"]["data"]=json
	return classTree
}
"""

htmltemplate="""
<html>
<head>
<title>Widoco Classtree</title>
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
<h1 align="center">OntologyView</h1>
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
	$('#jstree_demo_div').jstree(generateClassTree("class","has super-classes",true));
	$('#jstree_demo_div1').jstree(generateClassTree("named individual","belongs to",false));
	$('#jstree_demo_div2').jstree(generateClassTree("object property","has super-properties",false));
	$('#jstree_demo_div3').jstree(generateClassTree("data property","has super-properties",false));
	//$('#jstree_demo_div4').jstree(generateClassTree("annotation property",""));
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
    file.write(htmltemplate.replace("{{docfile}}",str(args.output)))
    