import random


class MemoryManager:
    def __init__(self, num_pages, page_size, num_frames):
        self.virtual_memory = num_pages * page_size
        self.page_table = [None] * num_pages
        self.physical_memory = [None] * num_frames
        self.hard_disk = {}  # Симулируем словарь, где ключи - номера страниц, а значения - содержимое страниц
        self.num_frames = num_frames
        self.page_size = page_size
        self.page_faults = 0

    def allocate_page(self, process_id, page_number):
        if self.page_table[page_number] is None:
            if None in self.physical_memory:
                frame_number = self.physical_memory.index(None)
            else:
                frame_number = self.page_replacement()
            self.page_table[page_number] = frame_number
            self.physical_memory[frame_number] = (process_id, page_number)
        return self.page_table[page_number]

    def page_replacement(self):
        # Простой алгоритм замещения страниц FIFO
        oldest_frame = self.physical_memory[0]
        page_to_remove = oldest_frame[1]
        frame_number = self.physical_memory.index(oldest_frame)
        self.hard_disk[page_to_remove] = f'Содержимое страницы {page_to_remove}'
        self.page_faults += 1
        return frame_number

    def access_memory(self, process_id, page_number):
        frame_number  = self.page_table[page_number]
        if frame_number  is None:
            frame_number  = self.allocate_page(process_id, page_number)
        return f'Процесс {process_id} обратился к странице {page_number} из фрейма {frame_number}'


    def generate_system_st(self):
        st = '\n'
        st += '-----------------------------------------------\n'
        st += 'Диспетчер задач\n'
        st += '-----------------------------------------------\n\n'

        st += 'Виртуальная память:\n'
        st += f'- Общий размер: {self.virtual_memory} бит\n\n'

        st += 'Физическая память:\n'
        st += f'- Всего фреймов: {self.num_frames}\n'
        st += f'- Размер фреймов: {self.page_size} бит\n\n'

        st += 'Таблица страниц:\n'
        for page_number, frame_number in enumerate(self.page_table):
            if frame_number is not None:
                process_id = self.physical_memory[frame_number][0]
                st += f'Страница {page_number}: - Процесс {process_id} -  Фрейм {frame_number}\n'
        st += '\n'

        st += 'Ошибки доступа к странице:\n'
        st += f'- Всего ошибок доступа к страницам: {self.page_faults}\n\n'

        st += 'Жёсткий диск:\n'
        for page_number, frame_number in enumerate(self.page_table):
            if frame_number is not None:
                process_id = self.physical_memory[frame_number][0]
                st += f'Фрейм {frame_number} содержит страницу {page_number} \n'
        st += '\n'

        print(st)

def main():
    num_pages = 16  # Количество страниц в виртуальном адресном пространстве
    page_size = 4096  # Размер страницы в байтах
    num_frames = 4  # Количество фреймов в физической памяти
    num_processes = 2 # Количество процессов

    memory_manager = MemoryManager(num_pages, page_size, num_frames)

    for process_id in range(num_processes):
        for i in range(20):  # Симулируем случайный доступ к страницам
            page_number = random.randint(0, num_pages - 1)
            print(memory_manager.access_memory(process_id, page_number))

    memory_manager.generate_system_st()

if __name__ == '__main__':
    main()
