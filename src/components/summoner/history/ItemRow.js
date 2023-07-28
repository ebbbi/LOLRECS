import React from "react";
import Image from "next/image";

function ItemRow({ details, index, items }) {
  return (
    <>
      {details[`item${index}`] ? (
        items
          .filter((i) => i.id === details[`item${index}`])
          .map((item, i) => (
            <img
              alt={item.id > 7000 ? item.name.split("%")[2] : item.name}
              src={`https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/items/icons2d/${item.iconPath
                .split("/")[6]
                .toLowerCase()}`}
            />
          ))
      ) : (
        <img
          alt="item"
          src="https://res.cloudinary.com/mistahpig/image/upload/v1621899018/league-stats/icons/emptyitem_cgiatq.png"
        />
      )}
    </>
  );
}

export default ItemRow;
