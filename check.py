from genie.testbed import load
from check_module import scheme_parse
from pyats import aetest
import re

tb = load('./testbed.yaml')

    
print()
scheme = scheme_parse('./ms.yaml')
criterion = scheme['criterions'][0]
subcriteria = criterion['subcriteria'][0]
print(f"+--- Criteria: {criterion['name']}")
print(f"+---+--- Subcriteria: {subcriteria['name']}")
class MarkingScheme(aetest.Testcase):
    @aetest.test.loop(aspect=subcriteria['aspects'])
    def subcriteria_check(self, steps, aspect):
        global tb
        print(f"+---+---+--- Aspect: {aspect['description']}")
        command = aspect['check']['action']['command']
        devices = aspect['check']['devices']
        values = aspect['check']['action']['values']
        with steps.start(f"+---+---+--- Aspect: {aspect['description']}") as step:
            is_expected = False
            for dev in devices:
                try:
                    tb.devices[dev].connect(mit=True, log_stdout=False)
                except:
                    continue
                output = tb.devices[dev].execute(command)
                print(output, values, sep='\n')
                for value in values:
                    if re.findall(value, output):
                        is_expected = True
            if is_expected:
                step.passed('Aspect passed')
            else:
                step.failed('Aspect failed')

if __name__ == "__main__":
    aetest.main()