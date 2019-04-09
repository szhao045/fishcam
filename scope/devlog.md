# Log

## z-stack problem

Due to the uneven attachment of the cells to the cover glass, it remains challenging of determining the z-stack for the image. The majority of the cells should be on the same plane, with minor difference, so the quick-and-dirty plan for automating the z-stack is to just set the max and min values of a given field, and get the rest of the z stack values automatically. 

## Syntax

* To call the scope object. First load the scope, then call scope_gui. 
* Ipython
* from scope import scope_client; scope = scope_client.ScopeClient()

## Recording the location

To avoid outputting crazily long file names, it is better to use a json database to store the metadata. 