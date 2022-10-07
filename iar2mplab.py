import logging
import argparse
import lxml.etree as ET
from copy import deepcopy

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'


class IarIdeParser():

    def __init__(self,input_file) -> None:
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(input_file, parser)
        root = tree.getroot()
        self.configurations = {}
        conf_list= []
        for config in root.iter('configuration'):
            conf_list.append(config.find("name").text)
        for conf in conf_list:
            self.configurations[conf] = {}
            cfg = root.findall(".//configuration[name='{}']/settings[name='ICCARM']/data/option[name='CCDefines']/state".format(conf))
            def_list=[]
            for i in cfg:
                def_list.append(i.text)
            self.configurations[conf]["define"]=def_list
            inc_list = []
            cfg = root.findall(".//configuration[name='{}']/settings[name='ICCARM']/data/option[name='CCIncludePath2']/state".format(conf))
            for i in cfg:
                inc_list.append(i.text)
            self.configurations[conf]["include"]=inc_list
            src_list = []
            cfg = root.findall(".//file/name")
            for i in cfg:
                src_list.append(i.text)
            self.configurations[conf]["source"]=src_list

class MplapConfig():
    def __init__(self, input_file) -> None:
        parser = ET.XMLParser(remove_blank_text=True)
        self.tree = ET.parse(input_file, parser)
        self.root = self.tree.getroot()

    
        self.configurations = {}
        conf_list= []
        for config in self.root.findall("confs/conf"):
            conf_list.append(config.get("name"))
 

        for conf in conf_list:
            self.configurations[conf] = {}
            def_C32 = self.root.find("confs/conf[@name='{}']/C32/property[@key='preprocessor-macros']".format(conf))
            def_list=def_C32.get("value").split(";")
            self.configurations[conf]["define"]=def_list

            inc_list = []
            inc_C32 = self.root.find("confs/conf[@name='{}']/C32/property[@key='extra-include-directories']".format(conf))
            inc_list = inc_C32.get("value").split(";")
            self.configurations[conf]["include"]=inc_list


            src_list = []
            for src in self.root.findall(".//logicalFolder[@name='SourceFiles']/itemPath"):
                src_list.append(src.text)
            self.configurations[conf]["source"]=src_list

    def set_src(self, src):
        s = self.root.find(".//logicalFolder[@name='SourceFiles']")
        for f in src:
            item = ET.Element('itemPath')
            item.text = f
            s.append(item)

    def set_inc(self, config, src):
        incelement = self.root.find("confs/conf[@name='{}']/C32/property[@key='extra-include-directories']".format(config))
        incelement.set('value',';'.join(src))

    def set_def(self, config, inc):
        defelement = self.root.find("confs/conf[@name='{}']/C32/property[@key='preprocessor-macros']".format(config))
        defelement.set('value',';'.join(inc))

    def duplicate_config(self, config, new_config_name):
        cfg = self.root.find("confs/conf[@name='{}']".format(config))
        new_cfg  = deepcopy(cfg)
        new_cfg.set("name",new_config_name)
        self.root.find("confs").append(new_cfg)

    def rename_config(self, config, new_config_name):
        cfg = self.root.find("confs/conf[@name='{}']".format(config))
        cfg.set("name",new_config_name)

    def delete_config(self, config):
        cfg = self.root.find("confs/conf[@name='{}']".format(config))
        self.root.remove(cfg)

    def migrate_iar_config(self, iar_config):
        for cfg in iar_config:
            print(cfg)
            self.duplicate_config('default', cfg)


    def export(self, outfile):
        self.tree.write(outfile,   pretty_print=True)




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Activate Debug mode with verbose execution trace information')
    parser.add_argument('--in', action='store')
    parser.add_argument('--out', action='store')
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
    mplab = MplapConfig("""C:\_work\polaris\lifeguard2_atomictests\_module_template\DUT\Template.X\\nbproject\configurations_template.xml""")
    print("MPLAB config : ",mplab.configurations)
    mplab.set_src( ['titi','toto'])
    mplab.set_inc('default',['inc1','inc2'])
    mplab.set_def('default',['PORT_API', '__design__'])
    mplab.duplicate_config('default','newconfig')
    mplab.rename_config('default','DEFAULT')
    mplab.migrate_iar_config(iar.configurations)
    mplab.export('toto.xml')    

 
