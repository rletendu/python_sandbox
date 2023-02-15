import logging
import argparse
import lxml.etree as ET
from copy import deepcopy
import os

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'

TEMPLATE_PROJECT_XML ="""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://www.netbeans.org/ns/project/1">
    <type>com.microchip.mplab.nbide.embedded.makeproject</type>
    <configuration>
        <data xmlns="http://www.netbeans.org/ns/make-project/1">
            <name></name>
            <creation-uuid/>
            <make-project-type>0</make-project-type>
            <c-extensions>c</c-extensions>
            <cpp-extensions/>
            <header-extensions/>
            <asminc-extensions/>
            <sourceEncoding>ISO-8859-1</sourceEncoding>
            <make-dep-projects/>
            <sourceRootList>
                <sourceRootElem>..</sourceRootElem>
            </sourceRootList>
            <confList>
                <confElem>
                    <name>default</name>
                    <type>2</type>
                </confElem>
            </confList>
            <formatting>
                <project-formatting-style>false</project-formatting-style>
            </formatting>
        </data>
    </configuration>
</project>
"""

class IarIdeParser():

    def __init__(self,input_file) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Parsing IAR file : {}".format(input_file))
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(input_file, parser)
        root = tree.getroot()
        self.configurations = {}
        conf_list= []
        for config in root.iter('configuration'):
            conf_list.append(config.find("name").text)
        for conf in conf_list:
            self.log.info("IAR Config : {}".format(conf))
            self.configurations[conf] = {}
            cfg = root.findall(".//configuration[name='{}']/settings[name='ICCARM']/data/option[name='CCDefines']/state".format(conf))
            def_list=[]
            for i in cfg:
                def_list.append(i.text)
            self.configurations[conf]["define"]=def_list
            self.log.info("IAR Config : {} Defines : {}".format(conf,def_list))
            inc_list = []
            cfg = root.findall(".//configuration[name='{}']/settings[name='ICCARM']/data/option[name='CCIncludePath2']/state".format(conf))
            for i in cfg:
                inc_list.append(i.text)
            self.configurations[conf]["include"]=inc_list
            self.log.info("IAR Config : {} Include Path : {}".format(conf, inc_list))
            src_list = []
            cfg = root.findall(".//file/name")
            for i in cfg:
                src_list.append(i.text)
            self.configurations[conf]["source"]=src_list
            self.log.info("IAR Config : {} Sources : {}".format(conf, src_list))



class MplabConfig():
    def __init__(self, input_file) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Parsing Mplab Configuration file {}".format(input_file))
        parser = ET.XMLParser(remove_blank_text=True)
        self.tree = ET.parse(input_file, parser)
        self.root = self.tree.getroot()
        self.configurations = {}
        conf_list= []
        for config in self.root.findall("confs/conf"):
            conf_list.append(config.get("name"))
 

        for conf in conf_list:
            self.log.info("Mplab Config : {}".format(conf))
            self.configurations[conf] = {}
            def_C32 = self.root.find("confs/conf[@name='{}']/C32/property[@key='preprocessor-macros']".format(conf))
            def_list=def_C32.get("value").split(";")
            self.configurations[conf]["define"]=def_list
            self.log.info("MPlab Config : {} Defines : {}".format(conf, def_list))

            inc_list = []
            inc_C32 = self.root.find("confs/conf[@name='{}']/C32/property[@key='extra-include-directories']".format(conf))
            inc_list = inc_C32.get("value").split(";")
            self.configurations[conf]["include"]=inc_list
            self.log.info("MPlab Config : {} Include Path : {}".format(conf, inc_list))


            src_list = []
            for src in self.root.findall(".//logicalFolder[@name='SourceFiles']/itemPath"):
                src_list.append(src.text)
            self.configurations[conf]["source"]=src_list
            self.log.info("MPlab Config : {} Sources : {}".format(conf, src_list))

    def set_src(self, src):
        s = self.root.find(".//logicalFolder[@name='SourceFiles']")
        for f in src:
            item = ET.Element('itemPath')
            sr = f.replace("$PROJ_DIR$\\","").replace("$PROJ_DIR$/","")
            item.text = sr
            self.log.info("Append Source files to MPlab : {}".format(sr))
            print("Append Source files to MPlab : {}".format(sr))
            if 'iar' in sr.lower():
                self.log.warning("!! Possible IAR specific file in {}".format(sr))
                print("!! Possible IAR specific file in {}".format(sr))
            s.append(item)

    def set_inc(self, config, inc_list):
        inc_element = self.root.find("confs/conf[@name='{}']/C32/property[@key='extra-include-directories']".format(config))
        inc = []
        for i in inc_list:
            fixed_inc = i.replace("$PROJ_DIR$\\", "").replace("$PROJ_DIR$/", "")
            print("Append Include Path {} from {}".format(fixed_inc,i))
            if 'iar' in fixed_inc.lower():
                print('Possible IAR reference in {}'.format(fixed_inc))
        inc_element.set('value',';'.join(inc))
        self.log.info("Mplab Config : {} Include Paths : {}".format(config,inc))

    def set_def(self, config, inc):
        def_element = self.root.find("confs/conf[@name='{}']/C32/property[@key='preprocessor-macros']".format(config))
        def_element.set('value',';'.join(inc))
        self.log.info("Mplab Config : {} Defines : {}".format(config, inc))

    def duplicate_config(self, config, new_config_name):
        self.log.info("Duplicating {} config in {}".format(config, new_config_name))
        cfg = self.root.find("confs/conf[@name='{}']".format(config))
        new_cfg  = deepcopy(cfg)
        new_cfg.set("name",new_config_name)
        self.root.find("confs").append(new_cfg)

    def rename_config(self, config, new_config_name):
        self.log.info("Renaming MPlab config {} to {}".format(config,new_config_name))
        cfg = self.root.find("confs/conf[@name='{}']".format(config))
        cfg.set("name",new_config_name)

    def delete_config(self, config):
        self.log.info("Removing MPlab config : {}".format(config))
        confs = self.root.find("confs")
        cfg = self.root.find("confs/conf[@name='{}']".format(config))
        confs.remove(cfg)

    def migrate_iar_config(self, iar_config):
        self.log.info("Migrating IAR to MPLab")
        for cfg in iar_config:
            self.duplicate_config('default', cfg)
            print("Implementing {} configuration".format(cfg))
            self.set_inc(cfg, iar_config[cfg]["include"])
            self.set_def(cfg, iar_config[cfg]["define"])
        self.set_src(iar_config[cfg]["source"])
        self.delete_config("default")


    def export(self, outfile):
        self.log.info("Writing MPlab Configuration to {}".format(outfile))
        self.tree.write(outfile, pretty_print=True)




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Activate Debug mode with verbose execution trace information')
    parser.add_argument('--in', action='store', help="The IAR input ewp file")
    parser.add_argument('--template', action='store', help="The MplabX configurations.xml input template file")
    parser.add_argument('--out', action='store', help="The MplabX configurations.xml output file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)
    log = logging.getLogger(__name__)

    if args.debug:
        log.setLevel(logging.DEBUG)
        log.info("Starting")
    else:
        log.setLevel(logging.CRITICAL)

    iar = IarIdeParser('C:\_work\polaris\lifeguard2_atomictests\_module_template\DUT\IAR\lifeguard_prj.ewp')
    print("IAR config : ",iar.configurations)
    mplab = MplabConfig("configurations_template.xml")
    print("MPLAB config : ",mplab.configurations)

    mplab.migrate_iar_config(iar.configurations)
    mplab.export(args.out)



    project_name = "titi"
    parser = ET.XMLParser(remove_blank_text=True)
    project_root = ET.fromstring(TEMPLATE_PROJECT_XML.encode(), parser)
    project_tree = ET.ElementTree(project_root)

    e_prj_name = project_root.find("project")
    print(e_prj_name, e_prj_name.text)
    e_prj_name.text = project_name
    project_tree.write("project.xml", pretty_print=True)
    dir = os.path.join(project_name,"nbproject")
    os.makedirs(dir)


 
