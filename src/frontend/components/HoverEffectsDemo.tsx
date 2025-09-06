import React from 'react';

const HoverEffectsDemo: React.FC = () => {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-8 text-center">
        🎯 Hover Efektleri Demo - "Buraya Tıklanır" Hissi
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Butonlar */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🔘 Butonlar</h2>
          
          <button className="btn-primary w-full py-3 px-6 bg-blue-600 text-white rounded-lg">
            Primary Button
          </button>
          
          <button className="btn-secondary w-full py-3 px-6 bg-gray-600 text-white rounded-lg">
            Secondary Button
          </button>
          
          <button className="btn-outline w-full py-3 px-6 border-2 border-blue-600 text-blue-600 rounded-lg">
            Outline Button
          </button>
        </div>

        {/* Linkler */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🔗 Linkler</h2>
          
          <a href="#" className="link-style block text-blue-600 text-lg">
            Normal Link
          </a>
          
          <a href="#" className="link-style block text-gray-600 text-lg">
            Secondary Link
          </a>
          
          <a href="#" className="link-style block text-green-600 text-lg">
            Success Link
          </a>
        </div>

        {/* Kartlar */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🃏 Kartlar</h2>
          
          <div className="card p-6 bg-white rounded-lg shadow-md border">
            <h3 className="font-semibold mb-2">Interactive Card</h3>
            <p className="text-gray-600">Bu kart hover edildiğinde yukarı kalkar</p>
          </div>
          
          <div className="card-interactive p-6 bg-gray-50 rounded-lg shadow-sm border">
            <h3 className="font-semibold mb-2">Hover Card</h3>
            <p className="text-gray-600">Hover efekti ile etkileşimli</p>
          </div>
        </div>

        {/* Menü Öğeleri */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📋 Menü Öğeleri</h2>
          
          <div className="menu-item p-3 bg-gray-100 rounded-lg">
            Ana Sayfa
          </div>
          
          <div className="nav-item p-3 bg-gray-100 rounded-lg">
            Hakkımızda
          </div>
          
          <div className="menu-item p-3 bg-gray-100 rounded-lg">
            İletişim
          </div>
        </div>

        {/* İkonlar */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🎨 İkonlar</h2>
          
          <div className="icon text-4xl text-gray-600 hover:text-blue-600">
            ⭐
          </div>
          
          <div className="icon-button text-4xl text-gray-600 hover:text-green-600">
            ❤️
          </div>
          
          <div className="icon text-4xl text-gray-600 hover:text-purple-600">
            🔔
          </div>
        </div>

        {/* Form Elementleri */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📝 Form Elementleri</h2>
          
          <input 
            type="text" 
            placeholder="Hover edin..." 
            className="input-field w-full p-3 border-2 border-gray-300 rounded-lg"
          />
          
          <textarea 
            placeholder="Bu alan da hover edilebilir..." 
            className="textarea-field w-full p-3 border-2 border-gray-300 rounded-lg h-20"
          />
        </div>

        {/* Tab'lar */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📑 Tab'lar</h2>
          
          <div className="tab p-3 bg-gray-100 rounded-lg text-center">
            Tab 1
          </div>
          
          <div className="tab-button p-3 bg-gray-100 rounded-lg text-center">
            Tab 2
          </div>
          
          <div className="tab p-3 bg-gray-100 rounded-lg text-center">
            Tab 3
          </div>
        </div>

        {/* Modal Butonları */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🪟 Modal Butonları</h2>
          
          <button className="modal-btn w-full py-3 px-6 bg-purple-600 text-white rounded-lg">
            Modal Aç
          </button>
          
          <button className="dialog-btn w-full py-3 px-6 bg-indigo-600 text-white rounded-lg">
            Dialog Aç
          </button>
        </div>

        {/* Dropdown Menüler */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📋 Dropdown</h2>
          
          <div className="dropdown-item p-3 bg-gray-100 rounded-lg">
            Seçenek 1
          </div>
          
          <div className="select-option p-3 bg-gray-100 rounded-lg">
            Seçenek 2
          </div>
          
          <div className="dropdown-item p-3 bg-gray-100 rounded-lg">
            Seçenek 3
          </div>
        </div>

        {/* Toggle Switch'ler */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🔀 Toggle</h2>
          
          <div className="toggle w-16 h-8 bg-gray-300 rounded-full relative">
            <div className="w-6 h-6 bg-white rounded-full absolute top-1 left-1 transition-transform"></div>
          </div>
          
          <div className="switch w-16 h-8 bg-gray-300 rounded-full relative">
            <div className="w-6 h-6 bg-white rounded-full absolute top-1 left-1 transition-transform"></div>
          </div>
        </div>

        {/* Progress Bar'lar */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📊 Progress</h2>
          
          <div className="progress-bar w-full h-4 bg-gray-300 rounded-full overflow-hidden">
            <div className="h-full bg-blue-600 rounded-full" style={{width: '60%'}}></div>
          </div>
          
          <div className="progress-bar w-full h-4 bg-gray-300 rounded-full overflow-hidden">
            <div className="h-full bg-green-600 rounded-full" style={{width: '80%'}}></div>
          </div>
        </div>

        {/* Tooltip'ler */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">💡 Tooltip</h2>
          
          <div className="tooltip-trigger p-3 bg-yellow-100 rounded-lg text-center">
            Hover edin (Tooltip)
          </div>
        </div>

        {/* Accordion */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📚 Accordion</h2>
          
          <div className="accordion-header p-3 bg-gray-100 rounded-lg">
            Bölüm 1
          </div>
          
          <div className="accordion-header p-3 bg-gray-100 rounded-lg">
            Bölüm 2
          </div>
        </div>

        {/* Breadcrumb */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🍞 Breadcrumb</h2>
          
          <div className="flex space-x-2">
            <span className="breadcrumb-item text-gray-500 hover:text-blue-600">Ana</span>
            <span className="text-gray-400">/</span>
            <span className="breadcrumb-item text-gray-500 hover:text-blue-600">Kategori</span>
            <span className="text-gray-400">/</span>
            <span className="breadcrumb-item text-gray-500 hover:text-blue-600">Ürün</span>
          </div>
        </div>

        {/* Pagination */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📄 Pagination</h2>
          
          <div className="flex space-x-2">
            <div className="page-item w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
              1
            </div>
            <div className="page-link w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
              2
            </div>
            <div className="page-item w-10 h-100 rounded-lg flex items-center justify-center">
              3
            </div>
          </div>
        </div>

        {/* Badge'ler */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🏷️ Badge'ler</h2>
          
          <span className="badge inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full">
            Yeni
          </span>
          
          <span className="tag inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full">
            Aktif
          </span>
        </div>

        {/* Avatar'lar */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">👤 Avatar'lar</h2>
          
          <div className="avatar w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
            A
          </div>
          
          <div className="profile-pic w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
            B
          </div>
        </div>

        {/* Notification'lar */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🔔 Bildirimler</h2>
          
          <div className="notification p-3 bg-blue-100 text-blue-800 rounded-lg">
            Yeni mesaj geldi
          </div>
          
          <div className="alert p-3 bg-yellow-100 text-yellow-800 rounded-lg">
            Dikkat! Önemli bilgi
          </div>
        </div>

        {/* Timeline */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">⏰ Timeline</h2>
          
          <div className="timeline-item p-3 bg-gray-100 rounded-lg">
            <div className="text-sm text-gray-500">10:00</div>
            <div>İlk görev tamamlandı</div>
          </div>
          
          <div className="timeline-item p-3 bg-gray-100 rounded-lg">
            <div className="text-sm text-gray-500">11:30</div>
            <div>İkinci görev başladı</div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📱 Sidebar</h2>
          
          <div className="sidebar-item p-3 bg-gray-100 rounded-lg">
            Dashboard
          </div>
          
          <div className="sidebar-link p-3 bg-gray-100 rounded-lg">
            Kullanıcılar
          </div>
        </div>

        {/* Header Navigation */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🧭 Header Nav</h2>
          
          <div className="header-nav-item p-3 bg-gray-100 rounded-lg text-center">
            Ana Sayfa
          </div>
          
          <div className="header-nav-item p-3 bg-gray-100 rounded-lg text-center">
            Hakkımızda
          </div>
        </div>

        {/* Footer Links */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🦶 Footer</h2>
          
          <div className="footer-link p-3 bg-gray-100 rounded-lg text-center">
            Gizlilik Politikası
          </div>
          
          <div className="footer-link p-3 bg-gray-100 rounded-lg text-center">
            Kullanım Şartları
          </div>
        </div>

        {/* Social Icons */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📱 Sosyal Medya</h2>
          
          <div className="social-icon text-4xl text-gray-600 hover:text-blue-600">
            📘
          </div>
          
          <div className="social-icon text-4xl text-gray-600 hover:text-blue-400">
            🐦
          </div>
          
          <div className="social-icon text-4xl text-gray-600 hover:text-red-600">
            📷
          </div>
        </div>

        {/* Loading Spinner */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🌀 Loading</h2>
          
          <div className="loading-spinner w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin">
          </div>
        </div>

        {/* Chart Elements */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📊 Grafik</h2>
          
          <div className="chart-element w-20 h-20 bg-blue-500 rounded-lg">
          </div>
          
          <div className="graph-item w-20 h-20 bg-green-500 rounded-lg">
          </div>
        </div>

        {/* Map Markers */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🗺️ Harita</h2>
          
          <div className="map-marker w-8 h-8 bg-red-500 rounded-full">
          </div>
          
          <div className="map-marker w-8 h-8 bg-blue-500 rounded-full">
          </div>
        </div>

        {/* Video Controls */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🎥 Video</h2>
          
          <div className="video-control w-12 h-12 bg-black bg-opacity-50 rounded-lg flex items-center justify-center text-white">
            ▶️
          </div>
          
          <div className="video-control w-12 h-12 bg-black bg-opacity-50 rounded-lg flex items-center justify-center text-white">
            ⏸️
          </div>
        </div>

        {/* Audio Controls */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🎵 Ses</h2>
          
          <div className="audio-control text-4xl text-gray-600">
            🔊
          </div>
          
          <div className="audio-control text-4xl text-gray-600">
            🔇
          </div>
        </div>

        {/* File Upload */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📁 Dosya</h2>
          
          <div className="file-upload-area w-full h-24 flex items-center justify-center text-gray-500">
            📁 Dosya yüklemek için tıklayın
          </div>
        </div>

        {/* Search Box */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🔍 Arama</h2>
          
          <div className="search-box w-full p-3 bg-gray-100 rounded-lg">
            🔍 Arama yapın...
          </div>
        </div>

        {/* Filter Buttons */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🔧 Filtreler</h2>
          
          <button className="filter-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            Tümü
          </button>
          
          <button className="filter-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            Aktif
          </button>
        </div>

        {/* Sort Buttons */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📊 Sıralama</h2>
          
          <button className="sort-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            A-Z
          </button>
          
          <button className="sort-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            Z-A
          </button>
        </div>

        {/* Export/Import */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">📤 Dışa/İçe Aktar</h2>
          
          <button className="export-btn w-full py-2 px-4 bg-green-600 text-white rounded-lg">
            📤 Dışa Aktar
          </button>
          
          <button className="import-btn w-full py-2 px-4 bg-blue-600 text-white rounded-lg">
            📥 İçe Aktar
          </button>
        </div>

        {/* Print/Share */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🖨️ Yazdır/Paylaş</h2>
          
          <button className="print-btn w-full py-2 px-4 bg-gray-600 text-white rounded-lg">
            🖨️ Yazdır
          </button>
          
          <button className="share-btn w-full py-2 px-4 bg-purple-600 text-white rounded-lg">
            📤 Paylaş
          </button>
        </div>

        {/* Bookmark/Like/Comment */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">❤️ Etkileşim</h2>
          
          <button className="bookmark-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            🔖 Kaydet
          </button>
          
          <button className="like-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            ❤️ Beğen
          </button>
          
          <button className="comment-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            💬 Yorum
          </button>
        </div>

        {/* Settings/Help/Info */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">⚙️ Yardım</h2>
          
          <button className="settings-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            ⚙️ Ayarlar
          </button>
          
          <button className="help-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            ❓ Yardım
          </button>
          
          <button className="info-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            ℹ️ Bilgi
          </button>
        </div>

        {/* Warning/Error/Success */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">⚠️ Durum</h2>
          
          <button className="warning-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            ⚠️ Uyarı
          </button>
          
          <button className="error-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            ❌ Hata
          </button>
          
          <button className="success-btn w-full py-2 px-4 bg-gray-200 rounded-lg">
            ✅ Başarı
          </button>
        </div>

        {/* Disabled Elements */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">🚫 Devre Dışı</h2>
          
          <button className="disabled w-full py-3 px-6 bg-gray-400 text-white rounded-lg">
            Devre Dışı Buton
          </button>
          
          <div className="disabled w-full p-3 bg-gray-200 rounded-lg">
            Devre Dışı Element
          </div>
        </div>

      </div>

      <div className="mt-12 p-6 bg-blue-50 rounded-lg">
        <h2 className="text-2xl font-bold mb-4 text-center">🎯 Nasıl Çalışır?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold mb-2">✨ Hover Efektleri:</h3>
            <ul className="list-disc list-inside space-y-1 text-gray-700">
              <li><strong>Transform:</strong> Yukarı kalkma, büyüme, döndürme</li>
              <li><strong>Box-shadow:</strong> Gölge efektleri</li>
              <li><strong>Color:</strong> Renk değişimleri</li>
              <li><strong>Background:</strong> Arka plan değişimleri</li>
              <li><strong>Border:</strong> Kenarlık efektleri</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">🚀 Avantajlar:</h3>
            <ul className="list-disc list-inside space-y-1 text-gray-700">
              <li><strong>Pointer olmadan</strong> etkileşim hissi</li>
              <li><strong>Görsel geri bildirim</strong> sağlar</li>
              <li><strong>Modern ve profesyonel</strong> görünüm</li>
              <li><strong>Erişilebilirlik</strong> artırır</li>
              <li><strong>Kullanıcı deneyimi</strong> iyileştirir</li>
            </ul>
          </div>
        </div>
      </div>

             <div className="mt-8 text-center text-gray-600">
         <p>💡 <strong>İpucu:</strong> Yukarıdaki elementlerin üzerine gelin ve hover efektlerini görün!</p>
                       <p>🎨 <strong>Not:</strong> Bu efektler pointer olmadan da "buraya tıklanır" hissi verir.</p>
              <p>🚫 <strong>Pointer:</strong> Artık tüm elementlerde varsayılan stil kullanılıyor!</p>
       </div>
    </div>
  );
};

export default HoverEffectsDemo;
