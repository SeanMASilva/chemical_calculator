from __future__ import annotations
from linkedlist import DoublLinkdList
from chemical_calculator import App, ElementList, MoleculeStorage
from ptable import ELEMENT_DICT, ELEMENTS, Element
import unittest

class TestCases(unittest.TestCase):
    
    base_app = App(testing=True)

    def test_History_ADT(self):
        
        histlist = DoublLinkdList()
        for i in range(10):
            histlist.append(i)
        for i in range (11,20):
            histlist.push(i)
        
        test_1st = []
        for item in histlist:
            test_1st.append(item)
        test_2nd = []
        for item in histlist:
            test_2nd.append(item)
        x = [one == two for one, two in zip(test_1st, test_2nd)]
        assert sum(x) == 19, "Cannot call linked list iterator twice"
        
        test_0 = []
        for item in histlist:
            test_0.append(item)
        test_9 = []
        histlist.change_iter_start(9)
        for item in histlist:
            test_9.append(item)
        
        for zero, nine in zip(test_0[9:14], test_9[0:5]):
            assert zero == nine, f"{zero} does not equal {nine}"
    
    def test_ElementList(self):
        h = ElementList(ELEMENT_DICT["H"])
        assert h.count["H"] == 1
        h2 = h*2
        assert h2.count["H"] == 2
        o = ElementList(ELEMENT_DICT["O"])
        h2o = h2+o
        assert h2o.count["H"] == 2
        assert h2o.count["O"] == 1
        h2o2 = h2o*2
        assert h2o2.count["H"] == 4
        assert h2o2.count["O"] == 2, f"got {h2o2.count['O']} instead"

        f = ElementList(ELEMENT_DICT["F"])
        f = f+None
        assert f.count["F"] == 1
        f = f*None
        assert f.count["F"] == 1
    
    def test_interpret_Elements(self):
        def basic_test():
            storage:MoleculeStorage = TestCases.base_app.user_commands.new_element(["new", "H2O"])
            assert storage.elements.count["H"] == 2
            assert storage.elements.count["O"] == 1
        def pre_mult_test():
            storage:MoleculeStorage = TestCases.base_app.user_commands.new_element(["new", "2NH3"])
            assert storage.elements.count["N"] == 2
            assert storage.elements.count["H"] == 6
        def bracket_test():
            storage:MoleculeStorage = TestCases.base_app.user_commands.new_element(["new", "Mg(OH)2"])
            assert storage.elements.count["Mg"] == 1
            assert storage.elements.count["O"] == 2
            assert storage.elements.count["H"] == 2
        def nested_brackets_test():
            storage:MoleculeStorage = TestCases.base_app.user_commands.new_element(["new", "3[Al(OH)2NH3]"])
            strings = ["Al", "O", "N", "H"]
            counts = [3, 6, 3, 15]
            for string, num in zip(strings, counts):
                assert storage.elements.count[string] == num, f"expected {num}{string} but got {storage.elements.count[string]}"

        tests = [basic_test, pre_mult_test, bracket_test, nested_brackets_test]

        for test in tests:
            with self.subTest(test.__name__):
                test()

    def test_change_molecule_info(self):
        test_mol = MoleculeStorage(["H", "2", "O", "(l)"], "H2O(l)")
        test_mol_mol_mass = test_mol.molar_mass
        test_mol.change_info("mass", test_mol_mol_mass)
        assert abs(test_mol.mass - test_mol_mol_mass) < 0.001
        assert abs(test_mol.moles - 1) < 0.001
        assert test_mol.volume is None
        assert test_mol.molarity is None
        assert test_mol.density is None

        test_mol.change_info("volume", 1)
        assert abs(test_mol.volume - 1) < 0.001
        assert abs(test_mol.molarity - 1) < 0.001
        assert abs(test_mol.density - test_mol_mol_mass) < 0.001

        try:
            test_mol.change_info("molarity", 1)
        except ValueError:
            pass
        else:
            assert False, "Molecule Storage does not raise a Value error when changing molarity, and propagating changes"
        


if __name__ == "__main__":
    unittest.main()