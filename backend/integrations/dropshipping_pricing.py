"""
Dropshipping Price Calculator
Automatic pricing with profit margins based on product cost
"""
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class DropshippingPriceCalculator:
    """
    Calculate selling prices for dropshipping products
    Based on profit margins by price range
    """
    
    # Profit margins by price range (from supplier price)
    MARGIN_RULES = [
        {"min": 0, "max": 50, "margin": 0.50},      # 50% profit for €1-€50
        {"min": 50, "max": 100, "margin": 0.45},    # 45% profit for €50-€100
        {"min": 100, "max": 200, "margin": 0.40},   # 40% profit for €100-€200
        {"min": 200, "max": 500, "margin": 0.30},   # 30% profit for €200-€500
        {"min": 500, "max": 999999, "margin": 0.25} # 25% profit for >€500
    ]
    
    def __init__(self):
        pass
    
    def calculate_selling_price(
        self,
        supplier_price: float,
        currency: str = "EUR"
    ) -> Dict[str, float]:
        """
        Calculate selling price based on supplier price
        
        Args:
            supplier_price: Price from supplier (AliExpress, Temu, etc.)
            currency: Currency code (EUR, USD, etc.)
        
        Returns:
            Dict with pricing details:
            {
                'supplier_price': 50.00,
                'margin_percentage': 0.50,
                'profit': 25.00,
                'selling_price': 75.00,
                'selling_price_rounded': 74.99
            }
        """
        # Find applicable margin rule
        margin = self._get_margin_for_price(supplier_price)
        
        # Calculate profit and selling price
        profit = supplier_price * margin
        selling_price = supplier_price + profit
        
        # Round to .99 for psychological pricing
        selling_price_rounded = self._round_to_99(selling_price)
        
        result = {
            'supplier_price': round(supplier_price, 2),
            'margin_percentage': margin,
            'profit': round(profit, 2),
            'selling_price': round(selling_price, 2),
            'selling_price_rounded': selling_price_rounded,
            'currency': currency
        }
        
        logger.info(
            f"Price calculated: €{supplier_price:.2f} → €{selling_price_rounded:.2f} "
            f"(margin: {margin*100:.0f}%, profit: €{profit:.2f})"
        )
        
        return result
    
    def _get_margin_for_price(self, price: float) -> float:
        """Get profit margin for a given price"""
        for rule in self.MARGIN_RULES:
            if rule['min'] <= price < rule['max']:
                return rule['margin']
        
        # Default to lowest margin if out of range
        return 0.25
    
    def _round_to_99(self, price: float) -> float:
        """
        Round price to psychological pricing (.99)
        Examples:
            75.50 → 74.99
            23.00 → 22.99
            99.00 → 98.99
        """
        import math
        
        # Get integer part
        integer_part = math.floor(price)
        
        # Return integer_part.99
        return float(f"{integer_part}.99")
    
    def calculate_bulk_prices(
        self,
        products: list
    ) -> list:
        """
        Calculate prices for multiple products
        
        Args:
            products: List of dicts with 'id', 'name', 'supplier_price'
        
        Returns:
            List of products with calculated prices
        """
        results = []
        
        for product in products:
            supplier_price = product.get('supplier_price', 0)
            
            if supplier_price <= 0:
                logger.warning(f"Invalid supplier price for product {product.get('name')}: {supplier_price}")
                continue
            
            pricing = self.calculate_selling_price(supplier_price)
            
            # Add pricing to product
            product_with_pricing = {
                **product,
                'pricing': pricing
            }
            
            results.append(product_with_pricing)
        
        return results
    
    def get_margin_info(self) -> list:
        """Get all margin rules"""
        return self.MARGIN_RULES
    
    def suggest_competitive_price(
        self,
        supplier_price: float,
        competitor_prices: list = None
    ) -> Dict:
        """
        Suggest competitive selling price
        
        Args:
            supplier_price: Your supplier price
            competitor_prices: List of competitor prices (optional)
        
        Returns:
            Dict with suggested price and analysis
        """
        # Calculate base price
        base_pricing = self.calculate_selling_price(supplier_price)
        
        if not competitor_prices:
            return {
                'suggested_price': base_pricing['selling_price_rounded'],
                'strategy': 'standard_margin',
                'base_pricing': base_pricing
            }
        
        # Analyze competition
        avg_competitor = sum(competitor_prices) / len(competitor_prices)
        min_competitor = min(competitor_prices)
        max_competitor = max(competitor_prices)
        
        suggested = base_pricing['selling_price_rounded']
        strategy = 'standard_margin'
        
        # Adjust based on competition
        if suggested > max_competitor:
            # We're too expensive
            suggested = self._round_to_99(max_competitor * 0.95)  # 5% below max
            strategy = 'competitive_pricing'
        
        elif suggested < min_competitor:
            # We can charge more
            suggested = self._round_to_99(avg_competitor)
            strategy = 'market_average'
        
        return {
            'suggested_price': suggested,
            'strategy': strategy,
            'base_pricing': base_pricing,
            'competition_analysis': {
                'avg': round(avg_competitor, 2),
                'min': min_competitor,
                'max': max_competitor
            }
        }


# Global instance
price_calculator = DropshippingPriceCalculator()


def calculate_price(supplier_price: float, currency: str = "EUR") -> Dict:
    """Helper function to calculate price"""
    return price_calculator.calculate_selling_price(supplier_price, currency)


def calculate_bulk(products: list) -> list:
    """Helper function for bulk calculation"""
    return price_calculator.calculate_bulk_prices(products)
