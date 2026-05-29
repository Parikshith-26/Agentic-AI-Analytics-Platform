class AgentMemory:

    _shared_memory = {}

    def __init__(self):

        self.memory = AgentMemory._shared_memory

    # ---------------------------------------------------
    # STORE VALUE
    # ---------------------------------------------------

    def store(

        self,

        key,

        value
    ):

        self.memory[key] = value

    # ---------------------------------------------------
    # RETRIEVE VALUE
    # ---------------------------------------------------

    def retrieve(

        self,

        key,

        default=None
    ):

        return self.memory.get(
            key,
            default
        )

    # ---------------------------------------------------
    # DELETE VALUE
    # ---------------------------------------------------

    def delete(self, key):

        if key in self.memory:

            del self.memory[key]

    # ---------------------------------------------------
    # CLEAR MEMORY
    # ---------------------------------------------------

    def clear(self):

        self.memory.clear()

    # ---------------------------------------------------
    # GET ALL MEMORY
    # ---------------------------------------------------

    def get_all(self):

        return self.memory

    # ---------------------------------------------------
    # GET RECENT CONTEXT
    # ---------------------------------------------------

    def get_recent_context(self):

        recent_items = list(
            self.memory.items()
        )[-5:]

        context = ""

        for key, value in recent_items:

            context += (
                f"{key}: {value}\n"
            )

        return context