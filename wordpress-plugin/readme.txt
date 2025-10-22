=== AI WooCommerce Agent ===
Contributors: tu-nombre
Tags: woocommerce, ai, automation, perplexity, openai, telegram, products
Requires at least: 6.0
Tested up to: 6.4
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Powerful AI agent for WooCommerce with Perplexity, OpenAI, automatic product management, Telegram bot, and 22+ integrated tools.

== Description ==

**AI WooCommerce Agent** is a revolutionary plugin that brings advanced artificial intelligence capabilities to your WooCommerce store.

= Key Features =

* **AI-Powered Product Optimization** - Automatically generate optimized descriptions, pricing, and images
* **Perplexity Integration** - Use Perplexity AI (sonar-pro) for advanced reasoning
* **OpenAI Integration** - GPT-4o for text generation and embeddings
* **Natural Language Commands** - Control your store with plain Spanish/English
* **Telegram Bot** - Manage your store from Telegram with commands
* **22+ Tools** - Product management, analytics, trend analysis, competition research
* **Memory System with RAG** - The AI remembers context and learns from interactions
* **Automated Workflows** - Set up automatic product processing
* **Analytics & Reports** - AI-powered insights about your store

= Use Cases =

* Optimize product descriptions for SEO
* Calculate optimal pricing based on market research
* Generate professional product images with AI
* Manage products via Telegram from anywhere
* Analyze market trends and competition
* Automate repetitive tasks
* Get intelligent insights about your store

= Supported Languages =

* Spanish (Español)
* English

= Requirements =

* WordPress 6.0+
* WooCommerce 7.0+
* PHP 7.4+
* At least one AI provider API key (Perplexity or OpenAI)

== Installation ==

1. Upload the `ai-woocommerce-agent` folder to `/wp-content/plugins/`
2. Activate the plugin through the 'Plugins' menu in WordPress
3. Go to **AI Agent > Settings** and configure your API keys
4. Start using natural language commands or process products with AI!

= Configuration =

1. **Get API Keys:**
   - Perplexity: https://perplexity.ai (Recommended)
   - OpenAI: https://platform.openai.com
   - Telegram Bot: Talk to @BotFather on Telegram

2. **Configure Settings:**
   - Navigate to **AI Agent > Settings**
   - Enter your API keys
   - Choose your AI provider (Perplexity recommended)
   - Enable Telegram Bot if needed
   - Save settings

3. **Test Connection:**
   - Click "Test Connection" in Settings
   - Verify all services are working

== Frequently Asked Questions ==

= Do I need all API keys? =

No. At minimum, you need either Perplexity OR OpenAI API key. Other services are optional.

= Is Perplexity better than OpenAI? =

Perplexity is recommended because it has access to real-time web data and provides more up-to-date information for market research and trend analysis.

= How much do the APIs cost? =

* Perplexity: Pay-as-you-go, typically $0.001 per 1K tokens
* OpenAI: GPT-4o costs around $2.50 per 1M input tokens
* Telegram: Free

= Can I use my own backend server? =

Yes! The plugin can work standalone with direct API calls, or connect to your FastAPI backend.

= Does it work with the standalone app? =

Yes! This plugin is fully compatible with the standalone FastAPI backend.

= How do I use Telegram commands? =

1. Configure your Telegram Bot Token in Settings
2. Send commands like:
   - `/procesar 123` - Process product ID 123
   - "Muéstrame productos sin precio" - Natural language
   - `/ayuda` - View help

= Is it compatible with my theme? =

Yes! The plugin only adds admin functionality and doesn't affect your frontend theme.

== Screenshots ==

1. Dashboard with real-time statistics
2. Command Center for natural language commands
3. Telegram Bot interface
4. Settings page with API configuration
5. Product edit page with AI optimization button

== Changelog ==

= 1.0.0 =
* Initial release
* AI-powered product optimization
* Perplexity and OpenAI integration
* Telegram Bot with natural language
* 22+ tools for WooCommerce management
* Memory system with RAG
* Automatic product processing
* Command Center interface
* Multi-language support (Spanish/English)

== Upgrade Notice ==

= 1.0.0 =
Initial release of AI WooCommerce Agent.

== Additional Information ==

= Privacy & Data =

This plugin sends product data to external AI services (Perplexity/OpenAI) for processing. Make sure this complies with your privacy policy.

= Support =

For support and documentation, visit: https://tu-dominio.com/soporte

= Contribute =

Development happens on GitHub: https://github.com/tu-usuario/ai-woocommerce-agent
