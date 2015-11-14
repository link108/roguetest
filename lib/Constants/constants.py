__author__ = 'cmotevasselani'


class Constants:
  # Inventory
  INVENTORY_WIDTH = 50

  #  Item
  CANCELLED = 'cancelled'

  # Scroll functions
  CONFUSE_RANGE = 8
  LIGHTNING_RANGE = 5
  LIGHTNING_DAMAGE = 40
  FIREBALL_RANGE = 6
  FIREBALL_RADIUS = 3
  FIREBALL_DAMAGE = 25

  # Potion functions
  HEAL_AMOUNT = 40

  # Game types
  BATTLE = 'battle'
  CRAWL = 'crawl'


  # Util
  TARGETING = 'targeting'
  FOUND_TARGET = 'found-target'
  PLAYING = 'playing'
  EXIT = 'exit'
  DEAD = 'dead'
  DID_NOT_TAKE_TURN = 'did-not-take-turn'
  NOT_VALID_KEY = 'not-valid-key'
  NEXT_LEVEL = 'next-level'
  PREVIOUS_LEVEL = 'previous-level'

  # File names
  DATA_DIR = 'data'
  SAVE_FILE = DATA_DIR + '/' + 'savefile.db'
  SPELL_FILE = DATA_DIR + '/' + 'spellfile'
  MONSTER_FILE = DATA_DIR + '/' + 'monsterfile'
  ITEM_FILE = DATA_DIR + '/' + 'itemfile'
  EQUIPMENT_FILE = DATA_DIR + '/' + 'equipmentfile'
  HIGH_SCORE_FILE = DATA_DIR + '/' + 'highscorefile.db'

  # MainMenu
  LEVEL_UP_BASE = 20
  LEVEL_UP_FACTOR = 70
  #  LEVEL_UP_BASE = 200
  #  LEVEL_UP_FACTOR = 150

  # Spells
  MAGIC_MISSILE = 'magic-missile'
  FROST_SHOCK = 'frost_shock'
  FROST_SHOCK_RANGE = 4
  FROST_SHOCK_DAMAGE = 20

  # Character creation
  PLAYER = 'player'
  # classes
  WARRIOR = 'Warrior'
  MAGE = 'Mage'
  ARCHER = 'Archer'

  # races
  ELF = 'Elf'
  HUMAN = 'Human'
  DWARF = 'Dwarf'

