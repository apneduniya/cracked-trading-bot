import typing as t

from pydantic import BaseModel, RootModel


class FirstPool(BaseModel):
    id: str
    createdAt: str


class Audit(BaseModel):
    mintAuthorityDisabled: t.Optional[bool] = None
    freezeAuthorityDisabled: t.Optional[bool] = None
    topHoldersPercentage: t.Optional[float] = None
    devBalancePercentage: t.Optional[float] = None


class Stats5m(BaseModel):
    holderChange: t.Optional[float] = None
    liquidityChange: t.Optional[float] = None
    buyVolume: t.Optional[float] = None
    sellVolume: t.Optional[float] = None
    buyOrganicVolume: t.Optional[float] = None
    sellOrganicVolume: t.Optional[float] = None
    numBuys: t.Optional[int] = None
    numSells: t.Optional[int] = None
    numTraders: t.Optional[int] = None


class Stats1h(BaseModel):
    holderChange: t.Optional[float] = None
    liquidityChange: t.Optional[float] = None
    volumeChange: t.Optional[float] = None
    buyVolume: t.Optional[float] = None
    sellVolume: t.Optional[float] = None
    buyOrganicVolume: t.Optional[float] = None
    sellOrganicVolume: t.Optional[float] = None
    numBuys: t.Optional[int] = None
    numSells: t.Optional[int] = None
    numTraders: t.Optional[int] = None


class Stats6h(BaseModel):
    priceChange: t.Optional[float] = None
    holderChange: t.Optional[float] = None
    liquidityChange: t.Optional[float] = None
    volumeChange: t.Optional[float] = None
    buyVolume: t.Optional[float] = None
    sellVolume: t.Optional[float] = None
    buyOrganicVolume: t.Optional[float] = None
    sellOrganicVolume: t.Optional[float] = None
    numBuys: t.Optional[int] = None
    numSells: t.Optional[int] = None
    numTraders: t.Optional[int] = None
    numOrganicBuyers: t.Optional[int] = None
    numNetBuyers: t.Optional[int] = None


class Stats24h(BaseModel):
    priceChange: t.Optional[float] = None
    holderChange: t.Optional[float] = None
    liquidityChange: t.Optional[float] = None
    volumeChange: t.Optional[float] = None
    buyVolume: t.Optional[float] = None
    sellVolume: t.Optional[float] = None
    buyOrganicVolume: t.Optional[float] = None
    sellOrganicVolume: t.Optional[float] = None
    numBuys: t.Optional[int] = None
    numSells: t.Optional[int] = None
    numTraders: t.Optional[int] = None
    numOrganicBuyers: t.Optional[int] = None
    numNetBuyers: t.Optional[int] = None


class TokenData(BaseModel):
    id: str  # The token's mint address
    name: str
    symbol: str
    icon: t.Optional[str] = None
    decimals: int
    dev: t.Optional[str] = None  # The token's developer address
    circSupply: t.Optional[float] = None
    totalSupply: t.Optional[float] = None
    tokenProgram: str  # The token program address
    launchpad: t.Optional[str] = None
    metaLaunchpad: t.Optional[str] = None
    partnerConfig: t.Optional[str] = None
    firstPool: t.Optional[FirstPool] = None
    holderCount: t.Optional[int] = None
    audit: t.Optional[Audit] = None
    organicScore: t.Optional[float] = None
    # Possible values: [high, medium, low]
    organicScoreLabel: t.Optional[str] = None
    isVerified: t.Optional[bool] = None
    cexes: t.Optional[list[str]] = None
    tags: t.Optional[list[str]] = None
    fdv: t.Optional[float] = None
    mcap: t.Optional[float] = None
    usdPrice: t.Optional[float] = None
    priceBlockId: t.Optional[int] = None
    liquidity: t.Optional[float] = None
    stats5m: t.Optional[Stats5m] = None
    stats1h: t.Optional[Stats1h] = None
    stats6h: t.Optional[Stats6h] = None
    stats24h: t.Optional[Stats24h] = None
    ctLikes: t.Optional[int] = None
    smartCtLikes: t.Optional[int] = None
    bondingCurve: t.Optional[float] = None
    updatedAt: str  # date-time


class TokenDataList(RootModel[t.List[TokenData]]):
    pass
