// The exported code uses Tailwind CSS. Install Tailwind CSS in your dev environment to ensure all styles work.
// start

import React, { useState } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination, Autoplay } from 'swiper/modules';

const App: React.FC = () => {
  const [selectedPlatform, setSelectedPlatform] = useState('All Platforms');
  const [selectedTimeframe, setSelectedTimeframe] = useState('This Week');
  const [showPlatformDropdown, setShowPlatformDropdown] = useState(false);

  const platforms = ['All Platforms', 'PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch'];
  const timeframes = ['Today', 'This Week', 'Next Month', 'Q2 2025', '2025'];

  const games = [
    {
      id: 1,
      title: 'Stellar Odyssey: Beyond the Void',
      genre: ['Action RPG', 'Sci-Fi'],
      releaseDate: '2025-03-15',
      rating: 9.4,
      description: 'An epic space adventure that combines intense combat with deep storytelling. Explore vast galaxies and uncover ancient mysteries.',
      imageUrl: 'https://public.readdy.ai/ai/img_res/5a6c2f643736eaf0042083d74f111cad.jpg'
    },
    {
      id: 2,
      title: 'Neon Knights: Cyber Revolution',
      genre: ['Cyberpunk', 'Action'],
      releaseDate: '2025-04-22',
      rating: 9.2,
      description: 'Dive into a neon-drenched cyberpunk world where hackers and mercenaries fight for control of the digital frontier.',
      imageUrl: 'https://public.readdy.ai/ai/img_res/339f9d10f21d12e72b4a35c19c6317bd.jpg'
    },
    {
      id: 3,
      title: 'Ancient Legends: Rise of Empires',
      genre: ['Strategy', 'Historical'],
      releaseDate: '2025-05-10',
      rating: 9.1,
      description: 'Build and manage your empire through the ages, from ancient civilizations to modern times.',
      imageUrl: 'https://public.readdy.ai/ai/img_res/fa8e5df5533ea59c815c34cc4767fbfc.jpg'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-6">Game Release Calendar</h1>
          
          <div className="flex flex-wrap gap-4 mb-6">
            <div className="relative">
              <button 
                onClick={() => setShowPlatformDropdown(!showPlatformDropdown)}
                className="!rounded-button bg-gray-800 px-4 py-2 flex items-center gap-2 hover:bg-gray-700 whitespace-nowrap"
              >
                {selectedPlatform} <i className="fas fa-chevron-down text-sm"></i>
              </button>
              
              {showPlatformDropdown && (
                <div className="absolute top-full mt-2 bg-gray-800 rounded-lg shadow-xl z-10">
                  {platforms.map((platform) => (
                    <button
                      key={platform}
                      onClick={() => {
                        setSelectedPlatform(platform);
                        setShowPlatformDropdown(false);
                      }}
                      className="block w-full text-left px-4 py-2 hover:bg-gray-700 whitespace-nowrap"
                    >
                      {platform}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div className="flex gap-2">
              {timeframes.map((timeframe) => (
                <button
                  key={timeframe}
                  onClick={() => setSelectedTimeframe(timeframe)}
                  className={`!rounded-button px-4 py-2 whitespace-nowrap ${
                    selectedTimeframe === timeframe
                      ? 'bg-yellow-600 text-white'
                      : 'bg-gray-800 hover:bg-gray-700'
                  }`}
                >
                  {timeframe}
                </button>
              ))}
            </div>
          </div>
        </header>

        <div className="grid gap-6">
          {games.map((game) => (
            <div
              key={game.id}
              className="bg-gray-800 rounded-lg overflow-hidden flex gap-6 p-6 hover:bg-gray-750 transition-colors"
            >
              <div className="w-[400px] h-[225px] relative flex-shrink-0">
                <img
                  src={game.imageUrl}
                  alt={game.title}
                  className="w-full h-full object-cover rounded-lg"
                />
              </div>
              
              <div className="flex-1">
                <div className="flex items-center gap-4 mb-2">
                  <span className="text-2xl font-bold text-yellow-500">#{game.id}</span>
                  <h3 className="text-2xl font-bold">{game.title}</h3>
                </div>
                
                <div className="flex gap-2 mb-4">
                  {game.genre.map((tag) => (
                    <span
                      key={tag}
                      className="px-3 py-1 bg-gray-700 rounded-full text-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="flex items-center gap-6 mb-4">
                  <div className="flex items-center gap-2">
                    <i className="fas fa-calendar text-yellow-500"></i>
                    <span>{game.releaseDate}</span>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <i className="fas fa-star text-yellow-500"></i>
                    <span className="font-bold">{game.rating}</span>
                  </div>
                </div>
                
                <p className="text-gray-300 line-clamp-2">{game.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
// end
