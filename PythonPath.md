## Introduction ##

After trying to get the App3Client to import correctly on my machine I ran into a few problems. All were missing packages or problems with my PythonPath, so here is how I fixed all of this.


## Mac OS X ##

**ImportError: No module named yaml**:
  * I didn't have yaml installed (and the website was down...) so I installed it from the Google package.
  * To fix:
```
python /Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/lib/yaml/setup.py install
```

**ImportError involving Google's libraries**:
  * I didn't have my PYTHONPATH environment variable set correctly
  * To fix (before you start Python in the terminal):
```
export PYTHONPATH=/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine:$PYTHONPATH
```

## Windows ##

**ImportError: No module named yaml**:
  * I didn't have yaml installed (and the website was down...) so I installed it from the Google package.
  * To fix:
```
cd "C:\Program Files\Google\google_appengine\lib\yaml\ "
python setup.py install
```