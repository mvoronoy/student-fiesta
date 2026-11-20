#include <iostream>
#include <string>
#include <vector>
#include <memory>

#ifdef _WIN32
#include <windows.h>
#endif

class PizzaOrder {
    std::string pizzaName;
    std::string crust;
    std::vector<std::string> extraIngredients;
    double price;

public:
    PizzaOrder(std::string pizzaName, std::string crust, double basePrice)
        : pizzaName(std::move(pizzaName)), crust(std::move(crust)), price(basePrice) {
    }

    std::unique_ptr<PizzaOrder> clone() const {
        return std::make_unique<PizzaOrder>(*this);
    }

    void addIngredient(const std::string& item, double cost) {
        extraIngredients.push_back(item);
        price += cost;
    }

    void print(const std::string& title) const {
        std::cout << "=== " << title << " ===\n"
            << "Піца: " << pizzaName << "\n"
            << "Бортик: " << crust << "\n"
            << "Додаткові інгредієнти: ";
        if (extraIngredients.empty()) {
            std::cout << "немає";
        }
        else {
            for (size_t i = 0; i < extraIngredients.size(); ++i)
                std::cout << extraIngredients[i] << (i + 1 < extraIngredients.size() ? ", " : "");
        }
        std::cout << "\nРазом: " << price << " грн\n\n";
    }
};

class PizzaFactory {
public:
    virtual ~PizzaFactory() = default;
    virtual std::unique_ptr<PizzaOrder> createPizza(const std::string& name, double basePrice) const = 0;
};

class RegularCrustPizzaFactory : public PizzaFactory {
public:
    std::unique_ptr<PizzaOrder> createPizza(const std::string& name, double basePrice) const override {
        return std::make_unique<PizzaOrder>(name, "Класичний бортик", basePrice);
    }
};

class CheeseCrustPizzaFactory : public PizzaFactory {
public:
    std::unique_ptr<PizzaOrder> createPizza(const std::string& name, double basePrice) const override {
        return std::make_unique<PizzaOrder>(name, "Сирний бортик (Моцарела)", basePrice + 65.0);
    }
};

class PizzeriaOrderFactory {
    PizzeriaOrderFactory() = default;

public:
    PizzeriaOrderFactory(const PizzeriaOrderFactory&) = delete;
    PizzeriaOrderFactory& operator=(const PizzeriaOrderFactory&) = delete;

    static PizzeriaOrderFactory& getInstance() {
        static PizzeriaOrderFactory instance;
        return instance;
    }

    std::unique_ptr<PizzaFactory> getStrategy(bool cheeseCrust) const {
        std::cout << "[Abstract Factory] Стратегія: "
            << (cheeseCrust ? "піца з сирним бортиком\n" : "піца зі звичайним бортиком\n");
        if (cheeseCrust) return std::make_unique<CheeseCrustPizzaFactory>();
        return std::make_unique<RegularCrustPizzaFactory>();
    }
};

class PizzaBuilder {
    std::unique_ptr<PizzaOrder> order;

public:
    PizzaBuilder& startPizza(const std::string& pizzaName, double basePrice, bool cheeseCrust) {
        auto factory = PizzeriaOrderFactory::getInstance().getStrategy(cheeseCrust);
        order = factory->createPizza(pizzaName, basePrice);
        std::cout << "[Builder] Обрано базову піцу: " << pizzaName << "\n";
        return *this;
    }

    PizzaBuilder& fromPrevious(const PizzaOrder& prev) {
        order = prev.clone();
        std::cout << "[Prototype] Скопійовано попередню піцу та її інгредієнти\n";
        return *this;
    }

    PizzaBuilder& addIngredient(const std::string& item, double cost) {
        order->addIngredient(item, cost);
        std::cout << "[Builder] + Інгредієнт: " << item << "\n";
        return *this;
    }

    std::unique_ptr<PizzaOrder> build() {
        return std::move(order);
    }
};

int main() {
#ifdef _WIN32
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
#endif

    PizzaBuilder builder;

    auto order1 = builder.startPizza("Маргарита", 180.0, true)
        .addIngredient("Подвійна моцарела", 40)
        .addIngredient("Томати чері", 30)
        .build();
    order1->print("Замовлення #1");

    auto order2 = builder.fromPrevious(*order1)
        .addIngredient("Пепероні", 45)
        .addIngredient("Халапеньйо", 25)
        .build();
    order2->print("Замовлення #2 (Prototype)");

    auto order3 = builder.startPizza("4 Сири", 240.0, false)
        .addIngredient("Груша", 35)
        .addIngredient("Волоський горіх", 30)
        .build();
    order3->print("Замовлення #3");

    return 0;
}