# Examples of design principles and patterns
- **Type safety**
Python is strongly typed (type conversion is explicit at runtime), just not statically typed. This means that type hints are not enforced and act more as mere suggestions.
- **Layered Architecture, Separation of Concerns, Encapsulation, Cohesion and Coupling:**
Divides the system into layers with distinct responsibilities. I did that for example with the folder structure of having entities handling the core elements, api clients to communicate with external world, and the teamgenerator containing the actual business logic.
- **Abstract Factory, DRY (Don't repeat yourself), Polymorphism:**
We created an abstract APIClient class, that can be inherited by different APIs that give us characters that can be converted to players.
- **Observer:** Defines a dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.
We use this in the front end. Whenever the teams change (new teams or new plan), we have to change how the canvas is drawn, and repopulate the players.
- **Encapsulation & immutability preference:**
All team related functionality is within the Team class. However, after its creation there's not much that can change other than the strategy (as the rest is private).
- **SOLID:**
    - **Single Responsibility Principle (SRP):**
    We do that for example with our Entity classes or the other ones. Classes both try to encapsulate all relevant to the entity, while doing one only thing.
    - **Open/Closed Principle (OCP):**
    We do that with the APIClient, which is closed for modification, but open for extension through adding new subclasses.
    - **Liskov Substitution Principle (LSP):**
    Subtypes must be substitutable for their base types, like SWAPIClient can be substituted by the APIClient
    - **Interface Segregation Principle (ISP):**
    Clients should not be forced to depend on interfaces they do not use. Same example as above, everything within APIClient is used by inherited classes.
    - **Dependency Inversion Principle (DIP):**
        - High-level modules should not depend on low-level modules; both should depend on abstractions.
        - Abstractions should not depend on details. Details should depend on abstractions.
    
        We do that with FastAPI working on with the abstraction layer of TeamGenerator and helpers to interact with high level modules (like Player, Team, or APIClients).

**For comedic purposes:**
    - **KISS (Keep It Simple, Stupid):**
    Kept everything simple. Structure, vanilla frontend, simple architecture.
    - **YAGNI (You Aren't Gonna Need It):**
    Description:** Don't add functionality until it's necessary. Didn't make the game playable!



# Potential things that could have been applied
- **Singleton:** The singleton pattern could have been used to ensure that we have only one instance of the SWAPIClient and only one of the PokeapiClient.

- **Adapter structure:** Player generation logic could move out of API clients. APIClients would then serve exclusively as means to interact with the external world. Now they are both clients and adapters (adapting external logic to our internal app). Then TeamGenerator would be the facilitator for interacting with everything. But of course all that was done intentionally,to avoid premature optimization.

