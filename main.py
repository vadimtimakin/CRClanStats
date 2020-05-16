# Main module.
import interaction_functions as ifu
import pickle_functions as pf
import warnings

# Ignore warnings.
warnings.filterwarnings("ignore")

ifu.start()
clan = pf.create_clan()
print(clan.title)
ifu.main_menu(clan)
