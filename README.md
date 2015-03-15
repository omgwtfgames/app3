# app3
App3 is a flexible REST interface to the AppEngine Datastore

----

 <h1><a name="Overview"></a>Overview<a href="#Overview" class="section_anchor"></a></h1><p>App3 is a flexible REST interface to the AppEngine Datastore that allows you to easily query models as REST resources. </p><h2><a name="Quick_Start"></a>Quick Start<a href="#Quick_Start" class="section_anchor"></a></h2><p>Included in App3 is a sample application that provides a single rest resource: &#x27;person&#x27;. To get it running quickly, download the sample application package in the featured downloads and run it in AppEngine.  </p><p>To check if you have the application up and running in AppEngine, try going to: <a href="http://localhost:8080/person/" rel="nofollow">http://localhost:8080/person/</a> in your browser. You should get an empty list displayed. </p><pre class="prettyprint">wget http://localhost:8080/person/ -O person.list
cat person.list
[]</pre><p>The demo DB is a read only database unless you provide the correct secret key (&#x27;correct_password&#x27;). All reading REST requests are permitted where write REST requests require authentication. </p><p>To easily put data into the datastore, you can use the provided REST client. If you have trouble with the following code, check out the <a href="/p/app3/wiki/PythonPath">PythonPath</a> page for help on setting up your AppEngine environment. </p><p>Once you have your Python path set, can do the following: </p><pre class="prettyprint">&gt;&gt;&gt; from app3.client import App3Client
&gt;&gt;&gt; client = App3Client(&#x27;localhost:8080&#x27;, &#x27;correct_password&#x27;) # Needed for authentication
&gt;&gt;&gt; client.list(&#x27;person&#x27;)
&gt;&gt;&gt; client.post(&#x27;person&#x27;, &#x27;tim&#x27;, {&#x27;age&#x27;: 24, &#x27;eyes&#x27;: &#x27;brown&#x27;})
&gt;&gt;&gt; client.get(&#x27;person&#x27;, &#x27;tim&#x27;)
&gt;&gt;&gt; client.list(&#x27;person&#x27;)
&gt;&gt;&gt; client.delete(&#x27;person&#x27;, &#x27;tim&#x27;)</pre><p>See the <a href="http://code.google.com/p/app3/wiki/Configuration" rel="nofollow">Configuration</a> page for more details on how to change the resources, secret key, etc. </p><h2><a name="Useful_Tools_with_App3"></a>Useful Tools with App3<a href="#Useful_Tools_with_App3" class="section_anchor"></a></h2><ul><li><strong>Note</strong>: After looking through the REST client library available, I felt that it was just too complicated and wrote a small sample client using httplib. It is in the svn trunk under the client directory and provided with App3 and the sample application. </li></ul>
