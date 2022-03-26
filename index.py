from IPython.display import display 
from PIL import Image
import random
import json
import os

os.system('cls' if os.name=='nt' else 'clear')

def create_new_image(all_images, config):
    new_image = {}
    for layer in config["layers"]:
      new_image[layer["name"]] = random.choices(layer["values"], layer["weights"])[0]
    
    for incomp in config["incompatibilities"]:
      for attr in new_image:
        if new_image[incomp["layer"]] == incomp["value"] and new_image[attr] in incomp["incompatible_with"]:
          return create_new_image(all_images, config)

    if new_image in all_images:
      return create_new_image(all_images, config)
    else:
      return new_image

def generate_unique_images(amount, config):
  print("Generating {} unique NFTs...".format(amount))
  pad_amount = len(str(amount))
  trait_files = {
  }
  for trait in config["layers"]:
    trait_files[trait["name"]] = {}
    for x, key in enumerate(trait["values"]):
      trait_files[trait["name"]][key] = trait["filename"][x]
  
  all_images = []
  for i in range(amount): 
    new_trait_image = create_new_image(all_images, config)
    all_images.append(new_trait_image)

  i = 1
  for item in all_images:
      item["tokenId"] = i
      i += 1

  for i, token in enumerate(all_images):
    attributes = []
    for key in token:
      if key != "tokenId":
        attributes.append({"trait_type": key, "value": token[key]})
    token_metadata = {
        "image": config["baseURI"] + "/images/" + str(token["tokenId"]) + '.png',
        "tokenId": token["tokenId"],
        "name":  config["name"] + str(token["tokenId"]).zfill(pad_amount),
        "description": config["description"],
        "attributes": attributes
    }
    with open('./metadata/' + str(token["tokenId"]) + '.json', 'w') as outfile:
        json.dump(token_metadata, outfile, indent=4)

  with open('./metadata/all-objects.json', 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
  
  for item in all_images:
    layers = []
    for index, attr in enumerate(item):
      if attr != 'tokenId':
        layers.append([])
        layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

    if len(layers) == 1:
      rgb_im = layers[0].convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) == 2:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) >= 3:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      layers.pop(0)
      layers.pop(0)
      for index, remaining in enumerate(layers):
        main_composite = Image.alpha_composite(main_composite, remaining)
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
  
  # v1.0.2 addition
  print("\nUnique NFT's generated. After uploading images to IPFS, please paste the CID below.\nYou may hit ENTER or CTRL+C to quit.")
  cid = input("IPFS Image CID (): ")
  if len(cid) > 0:
    if not cid.startswith("ipfs://"):
      cid = "ipfs://{}".format(cid)
    if cid.endswith("/"):
      cid = cid[:-1]
    for i, item in enumerate(all_images):
      with open('./metadata/' + str(item["tokenId"]) + '.json', 'r') as infile:
        original_json = json.loads(infile.read())
        original_json["image"] = original_json["image"].replace(config["baseURI"]+"/", cid+"/")
        with open('./metadata/' + str(item["tokenId"]) + '.json', 'w') as outfile:
          json.dump(original_json, outfile, indent=4)

generate_unique_images(50, {
  "layers": [
    {
      "name": "Accessory",
      "values": ["Bat", "Gold Chain", "Gold Rolex", "Intellect Serum", "Mace", "Mage", "Nether Raygun", "Popcorn", "Solana Flag"],
      "trait_path": "./trait-layers/accessories",
      "filename": ["bat.preview", "gold-chain.preview", "gold-rolex.preview", "intellect-serum.preview", "mace.preview", "mage.preview", "nether-raygun.preview", "popcorn.preview", "solana-flag.preview"],
      "weights": [40,10,10,10,10,5,5,5,5]
    },
    {
      "name": "Background",
      "values": ["Baby Blue", "Capri", "Cotton Candy", "Deep Champagne", "Lavender Blue", "Light Gray", "Magic Mint", "Mauve", "Platinum"],
      "trait_path": "./trait-layers/background",
      "filename": ["baby-blue.preview", "capri.preview", "cotton-candy.preview", "deep-champagne.preview", "lavender-blue.preview", "light-gray.preview", "magic-mint.preview", "mauve.preview", "platinum.preview"],
      "weights": [40,10,10,10,10,5,5,5,5]
    },
    {
      "name": "Clothes",
      "values": ["Astronaut Suit", "Football Jersey", "Jumpsuit", "Karate", "Mage", "My Name Is", "Police", "Toga", "Trenchcoat"],
      "trait_path": "./trait-layers/clothes",
      "filename": ["astronaut-suit.preview", "football-jersey.preview", "jumpsuit.preview", "karate.preview", "mage.preview", "my-name-is.preview", "police.preview", "toga.preview", "trenchcoat.preview"],
      "weights": [40,10,10,10,10,5,5,5,5]
    },
    {
      "name": "Expression",
      "values": ["Angry", "Excited", "Neutral", "Smile", "Stupid"],
      "trait_path": "./trait-layers/expression",
      "filename": ["angry.preview", "excited.preview", "neutral.preview", "smile.preview", "stupid.preview"],
      "weights": [20,20,20,20,20]
    },
    {
      "name": "Eyes",
      "values": ["Angry", "Excited", "Googly", "Neutral", "Smiling", "Stupid"],
      "trait_path": "./trait-layers/eyes",
      "filename": ["angry.preview", "excited.preview", "googly.preview", "neutral.preview", "smiling.preview", "stupid.preview"],
      "weights": [20,20,20,20,10,10]
    },
    {
      "name": "Headgear",
      "values": ["3D Glasses", "Astronaut Helmet", "Clown", "Dark Prince", "Fedora", "Halo", "Hardhat", "Headphones", "Officer"],
      "trait_path": "./trait-layers/headgear",
      "filename": ["3d-glasses.preview", "astronaut-helmet.preview", "clown.preview", "dark-prince.preview", "fedora.preview", "halo.preview", "hardhat.preview", "headphones.preview", "officer.preview"],
      "weights": [40,10,10,10,10,5,5,5,5]
    },
    {
      "name": "Skin",
      "values": ["Abstract", "Blue", "Camo Coral", "Camo Hot Pink", "Chrome Turquoise", "Damascus Steel", "Lava", "More Razzle", "Regular"],
      "trait_path": "./trait-layers/skin",
      "filename": ["abstract.preview", "blue.preview", "camo-coral.preview", "camo-hot-pink.preview", "chrome-turquoise.preview", "damascus-steel.preview", "lava.preview", "more-razzle.preview", "regular.preview"],
      "weights": [40,10,10,10,10,5,5,5,5]
    }
  ],
  "incompatibilities": [],
  "baseURI": ".",
  "name": "Snake #",
  "description": "This is Snake NFT Serie."
})

#Additional layer objects can be added following the above formats. They will automatically be composed along with the rest of the layers as long as they are the same size as eachother.
#Objects are layered starting from 0 and increasing, meaning the front layer will be the last object. (Branding)
