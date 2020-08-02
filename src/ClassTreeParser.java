

import java.util.List;
import java.util.Map;
import java.util.LinkedList;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.Queue;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

import org.json.JSONArray;
import org.json.JSONObject;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.AxiomType;
import org.semanticweb.owlapi.model.EntityType;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLAnnotation;
import org.semanticweb.owlapi.model.OWLAnnotationProperty;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLDataProperty;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLSubAnnotationPropertyOfAxiom;
import org.semanticweb.owlapi.model.OWLSubClassOfAxiom;
import org.semanticweb.owlapi.model.OWLSubObjectPropertyOfAxiom;
import org.semanticweb.owlapi.model.OWLSubPropertyAxiom;

public class ClassTreeParser {

	static BufferedWriter logwriter=null;
	
	/**The filepath to the icon of a class.*/
	public static String classimg="class.gif";	
	/**The filepath to the icon of a dataproperty.*/
	public static String datapropertyimg=".";
	/**The filepath to the icon of an objectproperty.*/	
	public static String objpropertyimg=".";
	
	
	private static JSONObject createClassTree( final OWLOntology model) {
	        Set<String> seenResources=new TreeSet<String>();
	        Set<String> workedResources=new TreeSet<String>();
	        JSONObject result=new JSONObject();
	        result.put("classes",new JSONArray());
	        result.put("objprop",new JSONArray());
	        result.put("dataprop",new JSONArray());
	        result.put("annoprop",new JSONArray());
	        result.put("individuals",new JSONArray());
	        System.out.println("SeenResources: "+seenResources);
	        System.out.println("WorkedResources: "+workedResources);
	        Iterator<OWLSubClassOfAxiom> sciter = model.axioms(AxiomType.SUBCLASS_OF).iterator();
	        System.out.println("Hasnext? "+sciter.hasNext());
	        while (sciter.hasNext())
        	{
	        	OWLSubClassOfAxiom subClasse=sciter.next();
        	    if (subClasse.getSuperClass() instanceof OWLClass 
        	         && subClasse.getSubClass() instanceof OWLClass)
        	    {       	
        	    	System.out.println(subClasse.getSuperClass().toString()+" - "+subClasse.getSubClass().toString());
        	    if(!seenResources.contains(subClasse.getSubClass().toString())){
            	    seenResources.add(subClasse.getSuperClass().toString());
            	    seenResources.add(subClasse.getSubClass().toString());
        	    		JSONObject treeelem=new JSONObject();
        	    		treeelem.put("id",subClasse.getSubClass().toString().replace("<", "").replace(">", ""));
        	    		treeelem.put("parent",subClasse.getSuperClass().toString().replace("<", "").replace(">", ""));
        	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif");
        	    		if(subClasse.getSubClass().toString().contains("#")) {
        	    			treeelem.put("text",subClasse.getSubClass().toString().substring(subClasse.getSubClass().toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
        	    		}else {
        	    			treeelem.put("text",subClasse.getSubClass().toString().substring(subClasse.getSubClass().toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
        	    		}
        	    		result.getJSONArray("classes").put(treeelem);
        	    		workedResources.add(subClasse.getSubClass().toString());
        	    }
        	    }
        	}
	        System.out.println("SeenResources: "+seenResources);
	        System.out.println("WorkedResources: "+workedResources);
	        for(String res:seenResources) {
	        	if(!workedResources.contains(res)) {
	        		System.out.println("Missing Class: "+res);
    	    		JSONObject treeelem=new JSONObject();
    	    		treeelem.put("id",res.replace("<", "").replace(">", ""));
    	    		treeelem.put("parent","#");
    	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif");
    	    		if(res.toString().contains("#")) {
    	    			treeelem.put("text",res.toString().substring(res.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
    	    		}else {
    	    			treeelem.put("text",res.toString().substring(res.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
    	    		}
    	    		result.getJSONArray("classes").put(treeelem);
	        	}
	        }
	        Iterator<OWLClass> classpropiter = model.classesInSignature().iterator();
	        System.out.println("Hasnext? "+sciter.hasNext());
	        while (classpropiter.hasNext()) {
	        	OWLClass c=classpropiter.next();
	        	if(!seenResources.contains(c.toString())) {
	        		JSONObject treeelem=new JSONObject();
		    		treeelem.put("id",c.toString().replace("<", "").replace(">", ""));
		    		treeelem.put("parent","#");
		    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif");
		    		if(c.toString().contains("#")) {
		    			treeelem.put("text",c.toString().substring(c.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
		    		}else {
		    			treeelem.put("text",c.toString().substring(c.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
		    		}
		    		result.getJSONArray("dataprop").put(treeelem);
	        	}
	        }
	        System.out.println(result.getJSONArray("classes").toString(2));
	        seenResources.clear();
	        workedResources.clear();
	        for (OWLClass c : model.getClassesInSignature()) {
	        	for (OWLNamedIndividual i :c.getIndividualsInSignature()) {
	        		JSONObject treeelem=new JSONObject();
    	    		treeelem.put("id",i.toString().replace("<", "").replace(">", ""));
    	    		treeelem.put("parent",c.toString().replace("<", "").replace(">", ""));
    	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif");
    	    		if(i.toString().contains("#")) {
    	    			treeelem.put("text",i.toString().substring(i.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
    	    		}else {
    	    			treeelem.put("text",i.toString().substring(i.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
    	    		}
    	    		result.getJSONArray("individuals").put(treeelem);
	        	}
	        }
	        Iterator<OWLSubObjectPropertyOfAxiom> sciter2 = model.axioms(AxiomType.SUB_OBJECT_PROPERTY).iterator();
	        System.out.println("Hasnext? "+sciter.hasNext());
	        while (sciter2.hasNext())
            	{
	        		OWLSubObjectPropertyOfAxiom subClasse = sciter2.next();
            	    if(!seenResources.contains(subClasse.getSuperProperty().toString())){
                	    seenResources.add(subClasse.getSuperProperty().toString());
                	    seenResources.add(subClasse.getSubProperty().toString());
            	    		JSONObject treeelem=new JSONObject();
            	    		treeelem.put("id",subClasse.getSubProperty().toString().replace("<", "").replace(">", ""));
            	    		treeelem.put("parent",subClasse.getSuperProperty().toString().replace("<", "").replace(">", ""));
            	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif");
            	    		if(subClasse.getSubProperty().toString().contains("#")) {
            	    			treeelem.put("text",subClasse.getSubProperty().toString().substring(subClasse.getSubProperty().toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
            	    		}else {
            	    			treeelem.put("text",subClasse.getSubProperty().toString().substring(subClasse.getSubProperty().toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
            	    		}
            	    		result.getJSONArray("objprop").put(treeelem);
            	    		workedResources.add(subClasse.getSubProperty().toString());
            	    }
            }
	        System.out.println(seenResources);
	        System.out.println(workedResources);
	        for(String res:seenResources) {
	        	if(!workedResources.contains(res)) {
	        		System.out.println("Missing ObjProp: "+res);
    	    		JSONObject treeelem=new JSONObject();
    	    		treeelem.put("id",res.replace("<", "").replace(">", ""));
    	    		treeelem.put("parent","#");
    	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif");
    	    		if(res.toString().contains("#")) {
    	    			treeelem.put("text",res.toString().substring(res.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
    	    		}else {
    	    			treeelem.put("text",res.toString().substring(res.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
    	    		}
    	    		result.getJSONArray("objprop").put(treeelem);
	        	}
	        }
	        Iterator<OWLObjectProperty> objpropiter = model.objectPropertiesInSignature().iterator();
	        System.out.println("Hasnext? "+sciter.hasNext());
	        while (objpropiter.hasNext()) {
	        	OWLObjectProperty c=objpropiter.next();
	        	if(!seenResources.contains(c.toString())) {
	        		JSONObject treeelem=new JSONObject();
    	    		treeelem.put("id",c.toString().replace("<", "").replace(">", ""));
    	    		treeelem.put("parent","#");
    	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif");
    	    		if(c.toString().contains("#")) {
    	    			treeelem.put("text",c.toString().substring(c.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
    	    		}else {
    	    			treeelem.put("text",c.toString().substring(c.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
    	    		}
    	    		result.getJSONArray("objprop").put(treeelem);
	        	}
	        }
	        seenResources.clear();
	        workedResources.clear();
	        for (final OWLSubPropertyAxiom subClasse : model.getAxioms(AxiomType.SUB_DATA_PROPERTY))
        	{
        	    if(!seenResources.contains(subClasse.getSuperProperty().toString())){
    	       	    seenResources.add(subClasse.getSuperProperty().toString());
            	    seenResources.add(subClasse.getSubProperty().toString());
        	    		JSONObject treeelem=new JSONObject();
        	    		treeelem.put("id",subClasse.getSubProperty().toString().replace("<", "").replace(">", ""));
        	    		treeelem.put("parent",subClasse.getSuperProperty().toString().replace("<", "").replace(">", ""));
        	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif");
        	    		if(subClasse.getSubProperty().toString().contains("#")) {
        	    			treeelem.put("text",subClasse.getSubProperty().toString().substring(subClasse.getSubProperty().toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
        	    		}else {
        	    			treeelem.put("text",subClasse.getSubProperty().toString().substring(subClasse.getSubProperty().toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
        	    		}
        	    		result.getJSONArray("dataprop").put(treeelem);
        	    		workedResources.add(subClasse.getSubProperty().toString());
        	    }
        }
	        System.out.println("SeenResources: "+seenResources);
	        System.out.println("WorkedResources: "+workedResources);
        for(String res:seenResources) {
        	if(!workedResources.contains(res)) {
        		System.out.println("Missing Dataprop: "+res);
	    		JSONObject treeelem=new JSONObject();
	    		treeelem.put("id",res.replace("<", "").replace(">", ""));
	    		treeelem.put("parent","#");
	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif");
	    		if(res.toString().contains("#")) {
	    			treeelem.put("text",res.toString().substring(res.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
	    		}else {
	    			treeelem.put("text",res.toString().substring(res.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
	    		}
	    		result.getJSONArray("dataprop").put(treeelem);
        	}
        }
        Iterator<OWLDataProperty> datapropiter = model.dataPropertiesInSignature().iterator();
        System.out.println("Hasnext? "+sciter.hasNext());
        while (datapropiter.hasNext()) {
        	OWLDataProperty c=datapropiter.next();
        	if(!seenResources.contains(c.toString())) {
        		JSONObject treeelem=new JSONObject();
	    		treeelem.put("id",c.toString().replace("<", "").replace(">", ""));
	    		treeelem.put("parent","#");
	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif");
	    		if(c.toString().contains("#")) {
	    			treeelem.put("text",c.toString().substring(c.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
	    		}else {
	    			treeelem.put("text",c.toString().substring(c.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
	    		}
	    		result.getJSONArray("dataprop").put(treeelem);
        	}
        }
        seenResources.clear();
        workedResources.clear();
        for (final OWLSubAnnotationPropertyOfAxiom subClasse : model.getAxioms(AxiomType.SUB_ANNOTATION_PROPERTY_OF))
    	{
    	    if(!seenResources.contains(subClasse.getSuperProperty().toString())){
           	    seenResources.add(subClasse.getSuperProperty().toString());
        	    seenResources.add(subClasse.getSubProperty().toString());
    	    		JSONObject treeelem=new JSONObject();
    	    		treeelem.put("id",subClasse.getSubProperty().toString().replace("<", "").replace(">", ""));
    	    		treeelem.put("parent",subClasse.getSuperProperty().toString().replace("<", "").replace(">", ""));
    	    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Annotation.gif");
    	    		if(subClasse.getSubProperty().toString().contains("#")) {
    	    			treeelem.put("text",subClasse.getSubProperty().toString().substring(subClasse.getSubProperty().toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
    	    		}else {
    	    			treeelem.put("text",subClasse.getSubProperty().toString().substring(subClasse.getSubProperty().toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
    	    		}
    	    		result.getJSONArray("annoprop").put(treeelem);
    	    		workedResources.add(subClasse.getSubProperty().toString());
    	    }
    }
        System.out.println("SeenResources: "+seenResources);
        System.out.println("WorkedResources: "+workedResources);
    for(String res:seenResources) {
    	if(!workedResources.contains(res)) {
    		System.out.println("Missing Annoprop: "+res);
    		JSONObject treeelem=new JSONObject();
    		treeelem.put("id",res.replace("<", "").replace(">", ""));
    		treeelem.put("parent","#");
    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Annotation.gif");
    		if(res.toString().contains("#")) {
    			treeelem.put("text",res.toString().substring(res.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
    		}else {
    			treeelem.put("text",res.toString().substring(res.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
    		}
    		result.getJSONArray("annoprop").put(treeelem);
    	}
    }
    Iterator<OWLAnnotationProperty> annopropiter = model.annotationPropertiesInSignature().iterator();
    System.out.println("Hasnext? "+sciter.hasNext());
    while (annopropiter.hasNext()) {
    	OWLAnnotationProperty c=annopropiter.next();
    	if(!seenResources.contains(c.toString())) {
    		JSONObject treeelem=new JSONObject();
    		treeelem.put("id",c.toString().replace("<", "").replace(">", ""));
    		treeelem.put("parent","#");
    		treeelem.put("icon","https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif");
    		if(c.toString().contains("#")) {
    			treeelem.put("text",c.toString().substring(c.toString().lastIndexOf('#')+1).replace("<", "").replace(">", ""));
    		}else {
    			treeelem.put("text",c.toString().substring(c.toString().lastIndexOf('/')+1).replace("<", "").replace(">", ""));
    		}
    		result.getJSONArray("annoprop").put(treeelem);
    	}
    }
    seenResources.clear();
    workedResources.clear();
    	return result;
	   }
	 
	 /*private static void printTree(List<List<OWLClass>> ress){
		 int i=0;
		 for(List<OWLClass> res:ress){
			 try {
				logwriter.write(i+": "+res.toString()+"\n");
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			 System.out.println(i+++": "+res.toString()+"\n");
		 }
	 }
	 
	 
	    public static String getClassHierarchyTree(OWLOntology model){
	        final Queue<List<OWLClass>> queue = new LinkedList<>();
	        final List<OWLClass> thingPath = new ArrayList<>();
	        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
	        OWLDataFactory factory = manager.getOWLDataFactory();
	        OWLClass entity = factory.getOWLEntity(EntityType.CLASS, IRI.create("http://www.w3.org/2002/07/owl#Thing"));
	        thingPath.add(entity);
	        queue.offer( thingPath );
	        try {
				logwriter=new BufferedWriter(new FileWriter(new File("debuglog.log")));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	        // Get the paths, and display them
	        final List<List<OWLClass>> paths = BFS( model, queue, 6 ,null);
	        printTree(paths);
	        try {
				logwriter.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	        return jsonExport(paths);
	    }
	 
	 private static String jsonExport(List<List<OWLClass>> hierarchy){
	    	int i=0,parent,level;
	    	String parentString="http://www.opengis.net/ont/geosparql#SpatialObject";
	    	Collections.reverse(hierarchy);
	    	StringBuilder builder=new StringBuilder();
	    	builder.append("{ \"plugins\": [\"search\", \"types\",\"sort\"],\"search\": {}, \"core\": { \"data\" :[");
	    	Set<String> idlist=new TreeSet<String>();
 		builder.append("{ \"id\" : \"http://www.w3.org/2002/07/owl#Thing\", \"parent\" : \"#\", \"text\" : \"owl:Thing\" },\n");
 		idlist.add("http://www.w3.org/2002/07/owl#Thing");
 		System.out.println("Hierarchy: "+hierarchy.toString());
	    	for(List<OWLClass> lres:hierarchy){
	    		parent=0;
	    		level=lres.size();
	    		for(OWLClass res:lres){
	    			if(res==null || res.getIRI()==null)
	    				continue;
	    			if(!idlist.contains(res.getIRI().toString())){
	    				builder.append("{ \"id\" : \""+res.getIRI()
	    						+"_"+level+
	    						"\", \"parent\" : \""+parentString/*+"_"+(level-1)
	    						+"\", \"text\" : \""+URLDecoder.decode(res.getIRI().getShortForm())+"\" },\n");
	    				idlist.add(res.getIRI().toString());
	    			}
	    			parentString=res.getIRI().toString();
 				parent++;
	    		}
	    		//BrokerOntologyConnection.log.debug("Idlist: "+idlist);
	    	}
	    	builder.delete(builder.length()-2, builder.length());
	    	builder.append("]},");
	    	builder.append("\"types\" : {\n\"file\" : {\n\"icon\" : \"../"+
	    			classimg+"\"\n},\"default\" : {\n\"icon\" : \"../"+
	    			classimg+"\",\n\"valid_children\" : [\"default\"]\n}\n}\n}");
	    	return builder.toString();
	    }*/
	 
	 public static void main(String[] args) throws OWLOntologyCreationException, IOException {
		 OWLOntologyManager manager = OWLManager.createOWLOntologyManager();

		 File file = new File("testont.ttl");

		 OWLOntology localAcademic = manager.loadOntologyFromOntologyDocument(file);
		 JSONObject res=createClassTree(localAcademic);
		 FileWriter writer=new FileWriter(new File("result.js"));
		 writer.write("var treedata="+res.toString(2));
		 writer.close();
	 }
		
}
