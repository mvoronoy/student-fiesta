#include <iostream>
#include <string>
#include <vector>
#include <memory>

using namespace std;

class Animal {
protected:
    string type;

public:
    Animal(const string& type) : type(type) {}

    virtual ~Animal() = default;

    string getType() const {
        return type;
    }

    virtual unique_ptr<Animal> clone() const = 0;
};

class Pet : public Animal {
public:
    Pet(const string& type)
        : Animal(type) {}

    unique_ptr<Animal> clone() const override {
        return make_unique<Pet>(*this);
    }
};

class AnimalFactory {
public:
    virtual ~AnimalFactory() = default;

    virtual unique_ptr<Animal> createAnimal(
        const string& type
    ) = 0;
};

class PetFactory : public AnimalFactory {
public:
    unique_ptr<Animal> createAnimal(
        const string& type
    ) override {

        return make_unique<Pet>(type);
    }
};

class Service {
protected:
    string name;

public:
    Service(const string& name)
        : name(name) {}

    virtual ~Service() = default;

    string getName() const {
        return name;
    }
};

class FeedingService : public Service {
public:
    FeedingService()
        : Service("Годування") {}
};


class CleaningService : public Service {
public:
    CleaningService()
        : Service("Прибирання місця проживання") {}
};


class WalkingService : public Service {
public:
    WalkingService()
        : Service("Прогулянка") {}
};


class VeterinaryService : public Service {
public:
    VeterinaryService()
        : Service("Ветеринарний контроль") {}
};

class ServiceCreator {
public:
    virtual ~ServiceCreator() = default;

    virtual unique_ptr<Service> createService() = 0;
};

class FeedingCreator : public ServiceCreator {
public:
    unique_ptr<Service> createService() override {
        return make_unique<FeedingService>();
    }
};


class CleaningCreator : public ServiceCreator {
public:
    unique_ptr<Service> createService() override {
        return make_unique<CleaningService>();
    }
};


class WalkingCreator : public ServiceCreator {
public:
    unique_ptr<Service> createService() override {
        return make_unique<WalkingService>();
    }
};


class VeterinaryCreator : public ServiceCreator {
public:
    unique_ptr<Service> createService() override {
        return make_unique<VeterinaryService>();
    }
};

class Order {
private:
    string ownerName;
    string animalName;
    string animalType;
    int days;

    vector<string> services;

public:

    Order()
        : days(0) {}

    void setOwnerName(const string& name) {
        ownerName = name;
    }

    void setAnimalName(const string& name) {
        animalName = name;
    }

    void setAnimalType(const string& type) {
        animalType = type;
    }

    void setDays(int numberOfDays) {
        days = numberOfDays;
    }

    void addService(const string& service) {
        services.push_back(service);
    }

    unique_ptr<Order> clone() const {
        return make_unique<Order>(*this);
    }

    void show() const {

        cout << "\n";
        cout << "========================================\n";
        cout << "           ВАШЕ ЗАМОВЛЕННЯ\n";
        cout << "========================================\n";

        cout << "Власник: " << ownerName << endl;
        cout << "Тип тварини: " << animalType << endl;
        cout << "Ім'я тварини: " << animalName << endl;
        cout << "Кількість днів: " << days << endl;

        cout << "\nПослуги:\n";

        if (services.empty()) {

            cout << "  Послуги не обрані.\n";

        } else {

            for (const string& service : services) {
                cout << "  + " << service << endl;
            }
        }

        cout << "========================================\n";
    }
};

class OrderBuilder {
private:
    unique_ptr<Order> order;

public:

    OrderBuilder() {
        order = make_unique<Order>();
    }

    OrderBuilder& setOwner(
        const string& name
    ) {

        order->setOwnerName(name);

        return *this;
    }

    OrderBuilder& setAnimal(
        const string& name,
        const string& type
    ) {

        order->setAnimalName(name);
        order->setAnimalType(type);

        return *this;
    }

    OrderBuilder& setDays(
        int numberOfDays
    ) {

        order->setDays(numberOfDays);

        return *this;
    }

    OrderBuilder& addService(
        unique_ptr<Service> service
    ) {

        order->addService(
            service->getName()
        );

        return *this;
    }

    unique_ptr<Order> build() {

        return move(order);
    }
};

class CatellFactoryManager {

private:
    CatellFactoryManager() {}

    CatellFactoryManager(
        const CatellFactoryManager&
    ) = delete;

    CatellFactoryManager& operator=(
        const CatellFactoryManager&
    ) = delete;

public:

    static CatellFactoryManager& getInstance() {

        static CatellFactoryManager instance;

        return instance;
    }

    unique_ptr<AnimalFactory> getAnimalFactory() {

        return make_unique<PetFactory>();
    }
};

unique_ptr<Order> previousOrder = nullptr;

void createNewOrder() {

    cout << "\n";
    cout << "========================================\n";
    cout << "          НОВЕ ЗАМОВЛЕННЯ\n";
    cout << "========================================\n";

    cout << "\n[1] SINGLETON\n";

    CatellFactoryManager& manager =
        CatellFactoryManager::getInstance();

    cout << "Отримано єдиний екземпляр Catell Factory.\n";

    cout << "\n[2] ABSTRACT FACTORY\n";

    string animalType;

    cout << "Введіть тип тварини ";
    cout << "(наприклад: кіт, папуга, кролик): ";

    cin >> animalType;

    auto animalFactory =
        manager.getAnimalFactory();

    auto animal =
        animalFactory->createAnimal(
            animalType
        );

    cout << "Створено тварину: "
         << animal->getType()
         << endl;

    string ownerName;
    string animalName;
    int days;

    cout << "\nВведіть ім'я власника: ";
    cin >> ownerName;

    cout << "Введіть ім'я тварини: ";
    cin >> animalName;

    cout << "Введіть кількість днів перетримки: ";
    cin >> days;

    cout << "\n[3] BUILDER\n";

    cout << "Поступово створюємо замовлення...\n";

    OrderBuilder builder;

    builder
        .setOwner(ownerName)
        .setAnimal(
            animalName,
            animal->getType()
        )
        .setDays(days);


    cout << "Основну інформацію додано.\n";

    cout << "\n[4] FACTORY METHOD\n";

    int serviceChoice;

    do {

        cout << "\n";
        cout << "========================================\n";
        cout << "               ПОСЛУГИ\n";
        cout << "========================================\n";

        cout << "1. Годування\n";
        cout << "2. Прибирання місця проживання\n";
        cout << "3. Прогулянка\n";
        cout << "4. Ветеринарний контроль\n";
        cout << "5. Завершити вибір\n";

        cout << "\nВаш вибір: ";
        cin >> serviceChoice;

        if (serviceChoice == 1) {

            FeedingCreator creator;

            auto service =
                creator.createService();

            cout << "+ Створено послугу: "
                 << service->getName()
                 << endl;

            builder.addService(
                move(service)
            );
        }

        else if (serviceChoice == 2) {

            CleaningCreator creator;

            auto service =
                creator.createService();

            cout << "+ Створено послугу: "
                 << service->getName()
                 << endl;

            builder.addService(
                move(service)
            );
        }

        else if (serviceChoice == 3) {

            WalkingCreator creator;

            auto service =
                creator.createService();

            cout << "+ Створено послугу: "
                 << service->getName()
                 << endl;

            builder.addService(
                move(service)
            );
        }

        else if (serviceChoice == 4) {

            VeterinaryCreator creator;

            auto service =
                creator.createService();

            cout << "+ Створено послугу: "
                 << service->getName()
                 << endl;

            builder.addService(
                move(service)
            );
        }

        else if (serviceChoice != 5) {

            cout << "Невірний вибір!\n";
        }

    } while (serviceChoice != 5);

    previousOrder =
        builder.build();


    cout << "\nЗамовлення успішно побудовано!\n";

    cout << "\n[5] FINAL RESULT\n";

    previousOrder->show();
}

void repeatPreviousOrder() {

    cout << "\n";
    cout << "========================================\n";
    cout << "       ПОВТОРЕННЯ ЗАМОВЛЕННЯ\n";
    cout << "========================================\n";

    if (previousOrder == nullptr) {

        cout << "\nПопереднього замовлення немає.\n";
        cout << "Спочатку створіть нове замовлення.\n";

        return;
    }

    cout << "\n[PROTOTYPE]\n";

    cout << "Знайдено попереднє замовлення.\n";
    cout << "Створюємо його копію...\n";

    auto newOrder =
        previousOrder->clone();

    cout << "Копію успішно створено!\n";

    cout << "\nНове замовлення:\n";

    newOrder->show();

    previousOrder =
        move(newOrder);
}

int main() {

    int choice;

    do {

        cout << "\n\n";

        cout << "========================================\n";
        cout << "      CATELL - ПЕРЕТРИМКА ТВАРИН\n";
        cout << "========================================\n";

        cout << "1. Створити нове замовлення\n";
        cout << "2. Повторити попереднє замовлення\n";
        cout << "3. Переглянути попереднє замовлення\n";
        cout << "0. Вийти\n";

        cout << "\nВаш вибір: ";
        cin >> choice;

        switch (choice) {

            case 1:

                createNewOrder();

                break;

            case 2:

                repeatPreviousOrder();

                break;

            case 3:

                if (previousOrder == nullptr) {

                    cout << "\n";
                    cout << "Попереднього замовлення немає.\n";

                } else {

                    cout << "\n";
                    cout << "========== ПОПЕРЕДНЄ ЗАМОВЛЕННЯ ==========\n";

                    previousOrder->show();
                }

                break;

            case 0:

                cout << "\n";
                cout << "Дякуємо за використання CATELL!\n";

                break;

            default:

                cout << "\n";
                cout << "Невірний вибір. Спробуйте ще раз.\n";
        }

    } while (choice != 0);

    return 0;
}
