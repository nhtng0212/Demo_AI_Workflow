class MiniStateGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.conditional_edges = {}

    def add_node(self, name: str, func):
        self.nodes[name] = func

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, condition_func):
        self.conditional_edges[from_node] = condition_func

    async def run(self, start_node: str, initial_state: dict):
        current_node = start_node
        state = initial_state

        while current_node != "END":
            print(f"\n[Graph] Đang chạy Node: '{current_node}")

            # 1.Node hiện tại nhận State, xử lý, và cập nhật State
            state = await self.nodes[current_node](state)

            # 2. Quyết định hướng đi tiếp theo
            if current_node in self.conditional_edges:
                current_node = self.conditional_edges[current_node](state)
            elif current_node in self.edges:
                current_node = self.edges[current_node]
            else:
                current_node = "END"

        print("\n[Graph] KẾT THÚC LUỒNG!")
        return state
