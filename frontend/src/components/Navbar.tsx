'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Menu, X, Sparkles, User, LogOut } from 'lucide-react';
import { useState } from 'react';
import { useAppStore } from '@/lib/store';

const navItems = [
  { href: '/', label: 'Home' },
  { href: '/scan', label: 'Scan' },
  { href: '/analyze', label: 'Analyze' },
  { href: '/compare', label: 'Compare' },
  { href: '/fuzzy-logic', label: 'Fuzzy Logic' },
  { href: '/claims', label: 'Claims' },
  { href: '/dashboard', label: 'Dashboard' },
];

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();
  const { user, logout } = useAppStore();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black/50 backdrop-blur-lg border-b border-white/10">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-2">
            <motion.div whileHover={{ rotate: 360 }} transition={{ duration: 0.5 }} className="w-10 h-10 bg-gradient-to-r from-pink-500 to-purple-500 rounded-xl flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </motion.div>
            <span className="text-xl font-bold gradient-text">CosmeticIQ</span>
          </Link>

          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href} className={`relative px-3 py-2 text-sm font-medium rounded-lg transition-colors ${pathname === item.href ? 'text-pink-400 bg-white/5' : 'text-gray-300 hover:text-white hover:bg-white/5'}`}>
                {item.label}
              </Link>
            ))}
          </div>

          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-4">
                <Link href="/profile" className="flex items-center space-x-2 text-gray-300 hover:text-white">
                  <User className="w-5 h-5" />
                  <span>{user.username}</span>
                </Link>
                <button onClick={logout} className="text-gray-300 hover:text-white"><LogOut className="w-5 h-5" /></button>
              </div>
            ) : (
              <>
                <Link href="/login" className="text-gray-300 hover:text-white transition-colors">Login</Link>
                <Link href="/register" className="glass-button text-sm py-2 px-4">Get Started</Link>
              </>
            )}
          </div>

          <button onClick={() => setIsOpen(!isOpen)} className="md:hidden text-gray-300">
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {isOpen && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="md:hidden py-4 border-t border-white/10">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href} onClick={() => setIsOpen(false)} className={`block py-2 px-4 rounded-lg ${pathname === item.href ? 'bg-white/10 text-pink-400' : 'text-gray-300 hover:bg-white/5'}`}>
                {item.label}
              </Link>
            ))}
            <div className="mt-4 pt-4 border-t border-white/10 px-4">
              {user ? (
                <button onClick={() => { logout(); setIsOpen(false); }} className="w-full text-left py-2 text-gray-300 hover:text-white">Logout</button>
              ) : (
                <div className="space-y-2">
                  <Link href="/login" onClick={() => setIsOpen(false)} className="block py-2 text-gray-300 hover:text-white">Login</Link>
                  <Link href="/register" onClick={() => setIsOpen(false)} className="block py-2 text-pink-400 hover:text-pink-300">Get Started</Link>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </div>
    </nav>
  );
}
