from app import Cliente, Loan



def test_init():

    testuser = Cliente("Mattia", "Contu", "1520", "1500", "500")
    assert str(Cliente.get) == "<bound method Cliente.get of <class 'app.Cliente'>>"
    assert testuser.balance == "500"
    assert testuser.get_cc == "1520"

def test_date():

    testprestito = Loan("15480", "CNTNHN93S06A218L", "80000", "12", "06/01/2024", "06/12/2024")
    assert testprestito.starting_date == "06/01/2024"
    assert testprestito.ending_date == "06/12/2024"
    assert testprestito.get_cc == "CNTNHN93S06A218L"








# https://www.freecodecamp.org/news/how-to-write-unit-tests-for-instance-methods-in-python/  link utile

