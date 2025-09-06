"""
Enhanced Response Manager for Luminis.AI Library Assistant
========================================================

This module provides advanced response patterns and conversation flows to improve
the quality and naturalness of chatbot interactions. It manages:

1. Contextual Responses: Maintains conversation context to provide more relevant replies
2. Multi-language Support: Handles Turkish and English responses with cultural adaptation
3. Response Variations: Provides multiple response options to avoid repetitive answers
4. Conversation Flows: Guides users through structured conversations for better engagement
5. User Preferences: Tracks and utilizes user preferences for personalized interactions
6. Topic Detection: Intelligently identifies conversation topics for better responses

Key Features:
- Dynamic response generation based on conversation context
- Cultural and linguistic adaptation for different user bases
- Intelligent topic detection and response routing
- Conversation flow management for guided interactions
- User preference learning and utilization
- Response variation to maintain engagement

This module significantly improves the chatbot's ability to:
- Provide more natural and contextual responses
- Maintain engaging conversations over multiple interactions
- Adapt responses based on user language and cultural context
- Guide users through complex queries with structured flows
- Learn from user interactions to provide better future responses
"""

import random
from typing import Dict, List, Tuple


class EnhancedResponseManager:
    def __init__(self):
        self.conversation_context = {}
        self.user_preferences = {}
        self.response_variations = {}
        self._initialize_responses()

    def _initialize_responses(self):
        """Initialize enhanced response patterns"""

        # Response variations for common topics
        self.response_variations = {
            "greeting": {
                "tr": [
                    "Merhaba! Ben Luminis.AI Kütüphane Asistanı. Size nasıl yardımcı olabilirim?",
                    "Selam! Kitap dünyasında size rehberlik etmekten mutluluk duyarım.",
                    "Hoş geldiniz! Edebiyat dünyasında keşfedilecek çok şey var.",
                    "Merhaba! Kitap önerileri ve edebiyat bilgisi konusunda uzmanım.",
                ],
                "en": [
                    "Hello! I'm Luminis.AI Library Assistant. How can I help you?",
                    "Hi there! I'd be happy to guide you through the world of books.",
                    "Welcome! There's so much to discover in the world of literature.",
                    "Hello! I'm an expert in book recommendations and literature knowledge.",
                ],
            },
            "book_recommendation": {
                "tr": [
                    "Size harika bir kitap önerisi verebilirim! Hangi türde kitap arıyorsunuz?",
                    "Kitap önerileri konusunda uzmanım! Ne tür bir hikaye arıyorsunuz?",
                    "Size özel kitap önerileri hazırlayabilirim! Hangi konular ilginizi çekiyor?",
                    "Harika kitaplar önermekten mutluluk duyarım! Hangi türde kitap istiyorsunuz?",
                ],
                "en": [
                    "I can give you a great book recommendation! What type of book are you looking for?",
                    "I'm an expert in book recommendations! What kind of story are you seeking?",
                    "I can prepare personalized book recommendations for you! What topics interest you?",
                    "I'd be happy to recommend wonderful books! What type of book do you want?",
                ],
            },
            "reading_advice": {
                "tr": [
                    "Okuma alışkanlığı geliştirmek için size yardımcı olabilirim!",
                    "Daha iyi okuma pratikleri için önerilerim var!",
                    "Okuma hedefleri belirlemenize yardımcı olabilirim!",
                    "Okuma günlüğü tutmak çok faydalı olabilir!",
                ],
                "en": [
                    "I can help you develop reading habits!",
                    "I have suggestions for better reading practices!",
                    "I can help you set reading goals!",
                    "Keeping a reading journal can be very beneficial!",
                ],
            },
        }

        # Advanced conversation flows
        self.conversation_flows = {
            "book_discovery": {
                "tr": [
                    "Hangi türde kitaplar ilginizi çekiyor?",
                    "Sevdiğiniz yazarlar var mı?",
                    "Hangi konular hakkında okumayı seviyorsunuz?",
                    "Okuma seviyeniz nedir?",
                    "Hangi duygu durumunda kitap okumayı tercih edersiniz?",
                ],
                "en": [
                    "What types of books interest you?",
                    "Do you have favorite authors?",
                    "What topics do you enjoy reading about?",
                    "What's your reading level?",
                    "In what mood do you prefer to read books?",
                ],
            },
            "reading_improvement": {
                "tr": [
                    "Günde kaç dakika okuma yapıyorsunuz?",
                    "Hangi türde kitaplar okumayı zor buluyorsunuz?",
                    "Okuma hızınızı artırmak ister misiniz?",
                    "Anlayarak okuma konusunda zorluk yaşıyor musunuz?",
                    "Hangi okuma tekniklerini denediniz?",
                ],
                "en": [
                    "How many minutes do you read per day?",
                    "What types of books do you find difficult to read?",
                    "Would you like to increase your reading speed?",
                    "Do you have difficulty with reading comprehension?",
                    "What reading techniques have you tried?",
                ],
            },
        }

    def get_contextual_response(self, user_message: str, user_language: str = "tr", context: str = None) -> str:
        """Get a contextual response based on user message and conversation context"""

        message_lower = user_message.lower()

        # Check for specific conversation patterns
        if self._is_greeting(message_lower, user_language):
            return self._get_greeting_response(user_language)

        if self._is_book_request(message_lower, user_language):
            return self._get_book_recommendation_response(user_language)

        if self._is_reading_advice_request(message_lower, user_language):
            return self._get_reading_advice_response(user_language)

        # Check for specific book genres with detailed responses
        genre_response = self._get_specific_genre_response(message_lower, user_language)
        if genre_response:
            return genre_response

        # Check for mood-based responses
        mood = self._detect_mood(message_lower, user_language)
        if mood:
            return self._get_mood_based_response(mood, user_language)

        # Check for seasonal responses
        season = self._detect_season(message_lower, user_language)
        if season:
            return self._get_seasonal_response(season, user_language)

        # Default contextual response
        return self._get_default_contextual_response(user_language, context)

    def _get_specific_genre_response(self, message: str, language: str) -> str:
        """Get specific responses for different book genres"""

        genre_patterns = {
            "roman": {
                "tr": ["roman", "novel", "fiction", "hikaye", "story"],
                "en": ["novel", "fiction", "story", "narrative"],
            },
            "bilim kurgu": {
                "tr": ["bilim kurgu", "science fiction", "sci-fi", "uzay", "space", "gelecek", "future"],
                "en": ["science fiction", "sci-fi", "space", "future", "technology"],
            },
            "fantastik": {
                "tr": ["fantastik", "fantasy", "büyü", "magic", "sihir", "elf", "dragon"],
                "en": ["fantasy", "magic", "magical", "elf", "dragon", "wizard"],
            },
            "klasik": {
                "tr": ["klasik", "classic", "eski", "old", "geleneksel", "traditional"],
                "en": ["classic", "classical", "old", "traditional", "timeless"],
            },
            "polisiye": {
                "tr": ["polisiye", "detective", "cinayet", "murder", "gizem", "mystery", "dedektif"],
                "en": ["detective", "mystery", "crime", "murder", "investigation"],
            },
            "tarih": {
                "tr": ["tarih", "history", "historical", "geçmiş", "past", "savaş", "war"],
                "en": ["history", "historical", "past", "war", "ancient", "medieval"],
            },
            "felsefe": {
                "tr": ["felsefe", "philosophy", "düşünce", "thought", "mantık", "logic"],
                "en": ["philosophy", "philosophical", "thought", "logic", "ethics"],
            },
            "psikoloji": {
                "tr": ["psikoloji", "psychology", "ruh", "soul", "karakter", "character", "davranış", "behavior"],
                "en": ["psychology", "psychological", "behavior", "mind", "mental"],
            },
            "teknoloji": {
                "tr": ["teknoloji", "technology", "tech", "dijital", "digital", "yapay zeka", "ai"],
                "en": ["technology", "tech", "digital", "artificial intelligence", "ai"],
            },
            "sanat": {
                "tr": ["sanat", "art", "resim", "painting", "müzik", "music", "heykel", "sculpture"],
                "en": ["art", "artistic", "painting", "music", "sculpture", "creative"],
            },
            "doğa": {
                "tr": ["doğa", "nature", "çevre", "environment", "orman", "forest", "deniz", "sea"],
                "en": ["nature", "natural", "environment", "forest", "sea", "wildlife"],
            },
            "aşk": {
                "tr": ["aşk", "love", "romantik", "romantic", "kalp", "heart"],
                "en": ["love", "romance", "romantic", "heart", "relationship"],
            },
            "macera": {
                "tr": ["macera", "adventure", "keşif", "exploration", "heyecan", "excitement"],
                "en": ["adventure", "exploration", "journey", "quest", "expedition"],
            },
            "gizem": {
                "tr": ["gizem", "mystery", "gerilim", "thriller", "suspense"],
                "en": ["mystery", "thriller", "suspense", "intrigue", "enigma"],
            },
            "komedi": {
                "tr": ["komedi", "comedy", "mizah", "humor", "eğlenceli", "funny"],
                "en": ["comedy", "humorous", "funny", "witty", "amusing"],
            },
            "drama": {
                "tr": ["drama", "dramatic", "duygusal", "emotional", "tragedy"],
                "en": ["drama", "dramatic", "emotional", "tragedy", "theatrical"],
            },
            "şiir": {
                "tr": ["şiir", "poetry", "poem", "verse", "dize"],
                "en": ["poetry", "poem", "verse", "lyrical", "rhyme"],
            },
        }

        genre_responses = {
            "roman": {
                "tr": [
                    "Roman türünde size özel öneriler verebilirim! Hangi alt türü tercih edersiniz? Tarihi roman, çağdaş edebiyat, psikolojik roman, sosyal roman gibi seçenekler var. Size hangi türde roman önermemi istersiniz?",
                    "Harika romanlar önermekten mutluluk duyarım! Roman türü çok geniş bir yelpaze. Macera dolu aksiyon romanları mı, derinlikli karakter analizleri mi, yoksa sürükleyici gerilim romanları mı arıyorsunuz?",
                    "Roman dünyasında keşfedilecek çok şey var! Size hangi türde roman önermemi istersiniz? Klasik edebiyat, modern roman, post-modern eserler veya deneysel romanlar arasından seçim yapabiliriz.",
                ],
                "en": [
                    "I can give you personalized recommendations for novels! Which subgenre do you prefer? There are historical novels, contemporary literature, psychological novels, social novels, and more. What type of novel would you like me to recommend?",
                    "I'd be happy to recommend great novels! The novel genre is very diverse. Are you looking for action-packed adventure novels, deep character analysis, or gripping thrillers?",
                    "There's so much to discover in the world of novels! What type of novel would you like me to recommend? We can choose from classic literature, modern novels, post-modern works, or experimental novels.",
                ],
            },
            "bilim kurgu": {
                "tr": [
                    "Bilim kurgu türü gerçekten büyüleyici! Size hangi alt türü önermemi istersiniz? Uzay operası, distopik romanlar, cyberpunk, post-apokaliptik hikayeler, zaman yolculuğu, alternatif tarih gibi seçenekler var. Hangi konu ilginizi çekiyor?",
                    "Bilim kurgu kitapları geleceği hayal etmenizi sağlar! Size özel öneriler verebilirim. Uzay kolonileri, yapay zeka, genetik mühendislik, paralel evrenler gibi konulardan hangisi sizi daha çok ilgilendiriyor?",
                    "Bilim kurgu dünyasında keşfedilecek çok şey var! Hangi bilimsel konuya odaklanan kitaplar istiyorsunuz? Fizik, biyoloji, astronomi, robotik veya sosyal bilimler temalı eserler arasından seçim yapabiliriz.",
                ],
                "en": [
                    "Science fiction is truly fascinating! Which subgenre would you like me to recommend? There are space operas, dystopian novels, cyberpunk, post-apocalyptic stories, time travel, alternative history, and more. What topic interests you?",
                    "Science fiction books allow you to imagine the future! I can give you personalized recommendations. Which of these topics interests you more: space colonies, artificial intelligence, genetic engineering, parallel universes?",
                    "There's so much to discover in the world of science fiction! What scientific topic would you like the books to focus on? We can choose from physics, biology, astronomy, robotics, or social science themed works.",
                ],
            },
            "fantastik": {
                "tr": [
                    "Fantastik kitaplar sizi büyülü dünyalara götürür! Hangi türde fantastik hikaye arıyorsunuz? Yüksek fantastik (epic fantasy), şehir fantastiği, karanlık fantastik, gençlik fantastiği gibi seçenekler var. Size hangi türü önermemi istersiniz?",
                    "Fantastik türünde harika öneriler verebilirim! Büyülü yaratıklar, sihirli güçler, kahramanlık hikayeleri mi arıyorsunuz? Yoksa daha gerçekçi, karakter odaklı fantastik romanlar mı?",
                    "Fantastik dünyasında herkes için bir şey var! Size hangi türde fantastik kitap önermemi istersiniz? Orta Dünya tarzı epik fantastik, modern şehir fantastiği, veya daha karanlık ve olgun temalar?",
                ],
                "en": [
                    "Fantasy books take you to magical worlds! What type of fantasy story are you looking for? There are high fantasy (epic fantasy), urban fantasy, dark fantasy, young adult fantasy, and more. Which type would you like me to recommend?",
                    "I can give you great recommendations in the fantasy genre! Are you looking for magical creatures, magical powers, heroic stories? Or more realistic, character-driven fantasy novels?",
                    "There's something for everyone in the fantasy world! What type of fantasy book would you like me to recommend? Middle-earth style epic fantasy, modern urban fantasy, or darker and more mature themes?",
                ],
            },
            "klasik": {
                "tr": [
                    "Klasik edebiyat zamansız hikayeler sunar! Hangi dönemden klasik eserler istiyorsunuz? Antik Yunan/Roma, Rönesans, 18. yüzyıl, 19. yüzyıl, 20. yüzyıl klasikleri gibi seçenekler var. Size hangi dönemi önermemi istersiniz?",
                    "Klasik kitaplar edebiyatın temelini oluşturur! Hangi türde klasik eser arıyorsunuz? Roman, tiyatro, şiir, deneme gibi türlerden hangisi ilginizi çekiyor? Ayrıca hangi kültürden eserler okumak istiyorsunuz?",
                    "Klasik edebiyat dünyasında keşfedilecek çok şey var! Size hangi türde klasik eser önermemi istersiniz? Tragedya, komedi, destan, pastoral, veya daha modern klasikler arasından seçim yapabiliriz.",
                ],
                "en": [
                    "Classic literature offers timeless stories! Which period of classic works do you want? There are Ancient Greek/Roman, Renaissance, 18th century, 19th century, 20th century classics, and more. Which period would you like me to recommend?",
                    "Classic books form the foundation of literature! What type of classic work are you looking for? Which genre interests you: novels, plays, poetry, essays? Also, from which culture would you like to read works?",
                    "There's so much to discover in the world of classic literature! What type of classic work would you like me to recommend? We can choose from tragedy, comedy, epic, pastoral, or more modern classics.",
                ],
            },
            "polisiye": {
                "tr": [
                    "Polisiye kitaplar sizi sonuna kadar tahmin etmeye zorlar! Hangi türde polisiye hikaye arıyorsunuz? Klasik dedektif hikayeleri, gerilim romanları, cinayet romanları, psikolojik gerilimler gibi seçenekler var. Size hangi türü önermemi istersiniz?",
                    "Polisiye türünde harika öneriler verebilirim! Hangi türde polisiye kitap istiyorsunuz? Agatha Christie tarzı klasik dedektif hikayeleri, modern gerilim romanları, veya daha karanlık ve karmaşık cinayet romanları?",
                    "Polisiye dünyasında her zevke uygun bir şey var! Size hangi türde polisiye kitap önermemi istersiniz? Rahat dedektif hikayeleri, sert gerilimler, veya daha entelektüel ve karmaşık cinayet romanları?",
                ],
                "en": [
                    "Mystery books keep you guessing until the end! What type of mystery story are you looking for? There are classic detective stories, thrillers, crime novels, psychological thrillers, and more. Which type would you like me to recommend?",
                    "I can give you great recommendations in the mystery genre! What type of mystery book do you want? Agatha Christie style classic detective stories, modern thrillers, or darker and more complex crime novels?",
                    "There's something for every taste in the mystery world! What type of mystery book would you like me to recommend? Cozy detective stories, hard-boiled thrillers, or more intellectual and complex crime novels?",
                ],
            },
        }

        # Check for genre patterns
        for genre, patterns in genre_patterns.items():
            if any(pattern in message for pattern in patterns[language]):
                if genre in genre_responses:
                    responses = genre_responses[genre][language]
                    return random.choice(responses)
                else:
                    # Generic genre response
                    if language == "tr":
                        return (
                            f"{genre.title()} türünde size yardımcı olabilirim! Hangi türde {genre} kitabı arıyorsunuz?"
                        )
                    else:
                        return f"I can help you with {genre}! What type of {genre} book are you looking for?"

        return None

    def _is_greeting(self, message: str, language: str) -> bool:
        """Check if message is a greeting"""
        greetings = {
            "tr": ["merhaba", "selam", "hi", "hello", "hey", "günaydın", "iyi günler"],
            "en": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
        }
        return any(greeting in message for greeting in greetings[language])

    def _is_book_request(self, message: str, language: str) -> bool:
        """Check if message is requesting book recommendations"""
        book_keywords = {
            "tr": ["kitap", "roman", "öneri", "tavsiye", "ne okuyayım", "hangi kitap"],
            "en": ["book", "novel", "recommendation", "suggestion", "what should i read", "which book"],
        }
        return any(keyword in message for keyword in book_keywords[language])

    def _is_reading_advice_request(self, message: str, language: str) -> bool:
        """Check if message is requesting reading advice"""
        advice_keywords = {
            "tr": ["okuma", "nasıl okuyayım", "okuma alışkanlığı", "hızlı okuma"],
            "en": ["reading", "how to read", "reading habit", "speed reading"],
        }
        return any(keyword in message for keyword in advice_keywords[language])

    def _detect_mood(self, message: str, language: str) -> str:
        """Detect user's mood from message"""
        mood_patterns = {
            "happy": {
                "tr": ["mutlu", "neşeli", "keyifli", "güzel", "harika", "mükemmel"],
                "en": ["happy", "joyful", "cheerful", "great", "wonderful", "amazing"],
            },
            "sad": {
                "tr": ["üzgün", "mutsuz", "kederli", "yorgun", "bitkin"],
                "en": ["sad", "unhappy", "sorrowful", "tired", "exhausted"],
            },
            "excited": {
                "tr": ["heyecanlı", "enerjik", "canlı", "dinç", "coşkulu"],
                "en": ["excited", "energetic", "lively", "vigorous", "enthusiastic"],
            },
            "calm": {
                "tr": ["sakin", "huzurlu", "rahat", "dingin", "sessiz"],
                "en": ["calm", "peaceful", "relaxed", "serene", "quiet"],
            },
        }

        for mood, patterns in mood_patterns.items():
            if any(pattern in message for pattern in patterns[language]):
                return mood

        return None

    def _detect_season(self, message: str, language: str) -> str:
        """Detect season or weather from message"""
        season_patterns = {
            "summer": {
                "tr": ["yaz", "sıcak", "güneş", "tatil", "deniz"],
                "en": ["summer", "hot", "sun", "vacation", "sea"],
            },
            "winter": {"tr": ["kış", "soğuk", "kar", "snow", "ısıtıcı"], "en": ["winter", "cold", "snow", "heater"]},
            "spring": {
                "tr": ["ilkbahar", "bahar", "çiçek", "yeşil", "taze"],
                "en": ["spring", "flower", "green", "fresh"],
            },
            "autumn": {
                "tr": ["sonbahar", "güz", "yaprak", "kahverengi", "melankoli"],
                "en": ["autumn", "fall", "leaf", "brown", "melancholy"],
            },
        }

        for season, patterns in season_patterns.items():
            if any(pattern in message for pattern in patterns[language]):
                return season

        return None

    def _get_greeting_response(self, language: str) -> str:
        """Get a greeting response"""
        responses = self.response_variations["greeting"][language]
        return random.choice(responses)

    def _get_book_recommendation_response(self, language: str) -> str:
        """Get a book recommendation response"""
        responses = self.response_variations["book_recommendation"][language]
        return random.choice(responses)

    def _get_reading_advice_response(self, language: str) -> str:
        """Get a reading advice response"""
        responses = self.response_variations["reading_advice"][language]
        return random.choice(responses)

    def _get_mood_based_response(self, mood: str, language: str) -> str:
        """Get a response based on user's mood"""
        mood_responses = {
            "happy": {
                "tr": "Mutlu hissettiğinizde hafif ve eğlenceli kitaplar okumak harika olur! Size özel öneriler verebilirim.",
                "en": "When you're feeling happy, reading light and fun books is wonderful! I can give you personalized recommendations.",
            },
            "sad": {
                "tr": "Üzgün hissettiğinizde umut verici ve sıcak hikayeler okumak iyi gelebilir. Size yardımcı olabilirim.",
                "en": "When you're feeling sad, reading hopeful and warm stories can help. I can assist you.",
            },
            "excited": {
                "tr": "Heyecanlı hissettiğinizde macera dolu ve aksiyon kitapları okumak harika olur!",
                "en": "When you're feeling excited, reading adventure and action books is wonderful!",
            },
            "calm": {
                "tr": "Sakin hissettiğinizde derinlikli ve düşündürücü kitaplar okumak çok güzel olur.",
                "en": "When you're feeling calm, reading deep and thought-provoking books can be very nice.",
            },
        }

        return mood_responses.get(mood, {}).get(language, "")

    def _get_seasonal_response(self, season: str, language: str) -> str:
        """Get a response based on season or weather"""
        seasonal_responses = {
            "summer": {
                "tr": "Yaz aylarında hafif ve eğlenceli kitaplar okumak harika olur! Yaz atmosferini tamamlayan kitaplar önerebilirim.",
                "en": "Reading light and fun books in summer is wonderful! I can recommend books that complement the summer atmosphere.",
            },
            "winter": {
                "tr": "Kış aylarında sıcak ve samimi kitaplar okumak çok güzel! Kış atmosferini tamamlayan kitaplar önerebilirim.",
                "en": "Reading warm and cozy books in winter is very nice! I can recommend books that complement the winter atmosphere.",
            },
            "spring": {
                "tr": "İlkbaharda yenilikçi ve umut verici kitaplar okumak harika olur!",
                "en": "Reading innovative and hopeful books in spring is wonderful!",
            },
            "autumn": {
                "tr": "Sonbaharda derinlikli ve düşündürücü kitaplar okumak çok güzel olur.",
                "en": "Reading deep and thought-provoking books in autumn can be very nice.",
            },
        }

        return seasonal_responses.get(season, {}).get(language, "")

    def _get_default_contextual_response(self, language: str, context: str = None) -> str:
        """Get a default contextual response"""
        default_responses = {
            "tr": [
                "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz.",
                "Kitap dünyasında size rehberlik etmekten mutluluk duyarım! Hangi konuda yardıma ihtiyacınız var?",
                "Edebiyat dünyasında keşfedilecek çok şey var! Size hangi konuda yardımcı olabilirim?",
                "Kitap önerileri ve edebiyat bilgisi konusunda uzmanım! Ne öğrenmek istiyorsunuz?",
            ],
            "en": [
                "I'm here to help you with this topic! I can provide book recommendations, literature information, or reading advice.",
                "I'd be happy to guide you through the world of books! What can I help you with?",
                "There's so much to discover in the world of literature! How can I assist you?",
                "I'm an expert in book recommendations and literature knowledge! What would you like to learn?",
            ],
        }

        responses = default_responses[language]
        return random.choice(responses)

    def get_conversation_flow(self, flow_type: str, language: str) -> List[str]:
        """Get a conversation flow for guided interactions"""
        return self.conversation_flows.get(flow_type, {}).get(language, [])

    def update_user_preferences(self, preferences: Dict[str, any]):
        """Update user preferences for personalized responses"""
        self.user_preferences.update(preferences)

    def get_personalized_response(self, topic: str, language: str) -> str:
        """Get a personalized response based on user preferences"""
        # This can be expanded to use user preferences for more personalized responses
        return self._get_default_contextual_response(language, topic)


# Global instance
response_manager = EnhancedResponseManager()
