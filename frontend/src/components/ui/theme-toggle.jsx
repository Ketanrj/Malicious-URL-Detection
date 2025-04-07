import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import * as DropdownMenu from '@radix-ui/react-dropdown-menu'

export function ThemeToggle() {
  const { setTheme } = useTheme()

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="inline-flex items-center justify-center rounded-md p-2 hover:bg-gray-100 dark:hover:bg-gray-800">
          <Sun className="h-5 w-5 rotate-0 scale-100 transition-transform dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-transform dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </button>
      </DropdownMenu.Trigger>
      <DropdownMenu.Content className="z-50 min-w-[8rem] overflow-hidden rounded-md border border-gray-200 bg-white p-1 shadow-md dark:border-gray-800 dark:bg-gray-950">
        <DropdownMenu.Item
          onClick={() => setTheme("light")}
          className="flex cursor-pointer items-center rounded-sm px-2 py-1.5 text-sm hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          Light
        </DropdownMenu.Item>
        <DropdownMenu.Item
          onClick={() => setTheme("dark")}
          className="flex cursor-pointer items-center rounded-sm px-2 py-1.5 text-sm hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          Dark
        </DropdownMenu.Item>
        <DropdownMenu.Item
          onClick={() => setTheme("system")}
          className="flex cursor-pointer items-center rounded-sm px-2 py-1.5 text-sm hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          System
        </DropdownMenu.Item>
      </DropdownMenu.Content>
    </DropdownMenu.Root>
  )
} 