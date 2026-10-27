#include <iostream>
#include <string>
#include <vector>

using namespace std;

class CrustOption {
public:
    virtual ~CrustOption() = default;
    virtual string getName() = 0;
    virtual int getPrice() = 0;
};

class StandardCrust : public CrustOption {
public:
    string getName() override { return "Звичайний бортик"; }
    int getPrice() override { return 0; }
};

class CheeseCrust : public CrustOption {
public:
    string getName() override { return "Сирний бортик"; }
    int getPrice() override { return 45; }
};

class CrustFactory {
private:
    StandardCrust standard;
    CheeseCrust cheese;

    CrustFactory() = default;

public:
    CrustFactory(const CrustFactory&) = delete;
    CrustFactory& operator=(const CrustFactory&) = delete;

    static CrustFactory& instance() {
        static CrustFactory inst;
        return inst;
    }

    CrustOption* selectCrust(bool withCheese) {
        if (withCheese) {
            return &cheese;
        }
        return &standard;
    }
};

class OrderTemplate {
public:
    vector<string> savedToppings;

    OrderTemplate(vector<string> toppings)
        : savedToppings(move(toppings)) {
    }

    vector<string> clone() const {
        return savedToppings;
    }
};

struct PizzaOrder {
    string title;
    string crust;
    vector<string> toppings;
    int totalPrice = 0;
};

class PizzaBuilder {
private:
    PizzaOrder order;

public:
    PizzaBuilder(string title, string crust, int basePrice) {
        order.title = title;
        order.crust = crust;
        order.totalPrice = basePrice;
    }

    void applyPrototypeToppings(const vector<string>& clonedToppings, int cost) {
        order.toppings = clonedToppings;
        order.totalPrice += cost;
    }

    void addTopping(const string& name, int cost) {
        order.toppings.push_back(name);
        order.totalPrice += cost;
    }

    PizzaOrder getResult() const {
        return order;
    }
};

class PizzaShop {
public:
    PizzaBuilder makePizzaBase(int choice, const string& crust, int crustPrice) {
        if (choice == 1) {
            return PizzaBuilder("Маргарита", crust, 120 + crustPrice);
        }
        return PizzaBuilder("Чотири сири", crust, 160 + crustPrice);
    }
};

int main() {
    string cheeseChoice;
    cout << "Бажаєте сирний бортик? (так/ні): ";
    cin >> cheeseChoice;

    bool wantCheese = (cheeseChoice == "так");
    CrustOption* crust = CrustFactory::instance().selectCrust(wantCheese);

    cout << "Обрано: " << crust->getName() << " (+" << crust->getPrice() << " грн)\n\n";

    int pizzaChoice = 1;
    cout << "Оберіть піцу (1 - Маргарита [120 грн], 2 - Чотири сири [160 грн]): ";
    cin >> pizzaChoice;

    PizzaShop shop;
    PizzaBuilder builder = shop.makePizzaBase(pizzaChoice, crust->getName(), crust->getPrice());

    OrderTemplate lastOrder({ "Базилік", "Подвійна моцарела" });
    string repeatChoice;
    cout << "Скопіювати улюблені інгредієнти з минулого замовлення? (так/ні): ";
    cin >> repeatChoice;

    if (repeatChoice == "так") {
        builder.applyPrototypeToppings(lastOrder.clone(), 35);
        cout << "-> Інгредієнти скопійовано!\n";
    }

    cout << "\nДодаткові топінги:\n";
    cout << "1 - Бекон (+30 грн)\n2 - Гриби (+20 грн)\n3 - Кукурудза (+15 грн)\n0 - Готово\n";

    while (true) {
        int topping = 0;
        cout << "Введіть номер: ";
        cin >> topping;

        if (topping == 0) break;

        if (topping == 1) builder.addTopping("Бекон", 30);
        else if (topping == 2) builder.addTopping("Гриби", 20);
        else if (topping == 3) builder.addTopping("Кукурудза", 15);
        else cout << "Невідомий пункт!\n";
    }

    PizzaOrder result = builder.getResult();

    cout << "\n========== ВАШЕ ЗАМОВЛЕННЯ ==========\n";
    cout << "Піца: " << result.title << "\n";
    cout << "Основа: " << result.crust << "\n";
    cout << "Склад: ";
    if (result.toppings.empty()) {
        cout << "стандартний набір";
    }
    else {
        for (size_t i = 0; i < result.toppings.size(); ++i) {
            cout << result.toppings[i] << (i + 1 < result.toppings.size() ? ", " : "");
        }
    }
    cout << "\nРазом до сплати: " << result.totalPrice << " грн\n";
    cout << "=====================================\n";

    return 0;
}