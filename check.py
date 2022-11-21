from genie.testbed import load
from check_module import scheme_parse, check_out
from pyats import aetest
import re
import logging

logger = logging.getLogger(__name__)

tb = load('./testbed.yaml')

    
print()
scheme = scheme_parse('./ms.yaml')
criterion = scheme['criterions'][0]
subcriteria = criterion['subcriteria'][0]
class Criteria_C(aetest.Testcase):
    @aetest.test.loop(aspect=subcriteria['aspects'])
    def subcriteria_check(self, steps, aspect):
        global tb
        
        commands = aspect['check']['action']['commands']
        devices = aspect['check']['devices']
        values = aspect['check']['action']['values']
        
        with steps.start(f"+---+---+--- Aspect: {aspect['name']} - {aspect['description']}") as step:
            is_expected = True
            for dev in devices:
                try:
                    tb.devices[dev].connect(mit=True, log_stdout=False)
                except:
                    is_expected = False
                    break
                for command in commands:
                    output = tb.devices[dev].execute(command)
                    logger.error(f"DEVICE --{dev}-- OUT")
                    if not check_out(values, output):
                        is_expected = False
                        break
                if not is_expected:
                    break
                
            if is_expected:
                step.passed('Aspect passed')
            else:
                step.failed('Aspect failed')
            

if __name__ == "__main__":
    aetest.main()