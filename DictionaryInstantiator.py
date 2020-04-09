import os
## private class like
class DictionaryExplorer:
         
    def __init__(self,basefolder):
        #Set the current path as the base folder of all circuits
        self.currentpath_str = basefolder
    

    def recursive_dictglobalexplorer(self,dir):
        currentpath_str = self.currentpath_str
        def recursive_dictlocalexplorer(currentpath_str,dir):
            realname = dir['namestandard']
            maskname = dir['alias']
            #initialize the current child number as 0 (there may be no child whatsoever)
            child_i = 0
            #try to get the number of child folders inside the list of dictionaries associated with the key value "children". 
            try:
                children_nr = len(dir['children'])
            #if it is None, a TypeError will be thrown, and the children nr will be 0
            except TypeError:
                children_nr = 0
            #Then, instead of throwing two dictionaries (dirpath_dict and filepath_dict) around throughout the 
            #several calls of recursive_dictlocalexplorer, we will instead have them as instance variables, rather
            #than local variables
            local_dict = {}
            local_dict[realname]={}

            #information that will be used in this directory and child directories
            currentpath_str = os.path.join(currentpath_str,maskname)
            if not os.path.exists(currentpath_str):
                if os.path.isdir(currentpath_str):
                    os.path.mkdir(currentpath_str)
            local_dict[realname]['path'] = currentpath_str
            partialdict = {}
            while child_i < children_nr:
                subdir = dir['children'][child_i]
                _,childdict = recursive_dictlocalexplorer(currentpath_str,subdir)
                partialdict.update(childdict)
                child_i+=1
            local_dict[realname].update(partialdict)
            
            #information in this directory
            if dir['filesystem'] is not None:
                local_dict[realname]['filepathdicts'] = {}
                try:
                     for key_namestandard in dir['filesystem']:
                       filename = dir['filesystem'][key_namestandard]
                       filepath = os.path.join(local_dict[realname]['path'],filename)
                       local_dict[realname]['filepathdicts'][key_namestandard] = filepath
                except:
                     print("The directory structure has errors.")
            else:
                local_dict[realname]['filepathdicts'] = {}
            return currentpath_str,local_dict

        _,self.dirpath_dict = recursive_dictlocalexplorer(currentpath_str,dir)
        return self.dirpath_dict



